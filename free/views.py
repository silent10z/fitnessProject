import json
import mimetypes
import os
import urllib

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.db.models import Q

from users.decorators import login_message_required
from users.models import User
from .forms import FreeWriterForm
from .models import Free, Comment


# 뷰 리스트 
class FreeListView(generic.ListView):
    model = Free
    paginate_by = 10
    template_name = 'free/free_list.html'
    context_object_name = 'free_list'

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        free_list = Free.objects.order_by('-id')

        if search_keyword:
            if len(search_keyword)> 1:
                if search_type == 'all':
                    search_notice_list = free_list.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword) | Q(
                            writer__username__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_notice_list = free_list.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = free_list.filter(title__icontains=search_keyword)
                elif search_type == 'content':
                    search_notice_list = free_list.filter(content__icontains=search_keyword)
                elif search_type == 'writer':
                    search_notice_list = free_list.filter(writer__username__icontains=search_keyword)

                return search_notice_list
            
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요')
        return free_list



    # 페이징 커스텀
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        free_fixed = Free.objects.filter(top_fixed=True).order_by('-registered_date')
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type
        context['free_fixed'] = free_fixed

        return context


# 게시판 디테일 뷰
@login_message_required
def free_detail_view(request, pk):

    free = get_object_or_404(Free, pk=pk)
    # 본인 게시글 확인 context
    if request.user == free.writer:
        free_auth = True
    else:
        free_auth = False

    session_cookie = request.session['email']
    cookie_name = F'free_hits:{session_cookie}'
    
    # 댓글 값 보내기
    comment = Comment.objects.filter(post=pk).order_by('created')
    comment_count = comment.exclude(deleted=True).count()
    context = {
        'free': free,
        'free_auth': free_auth,
        'comments': comment,
        'comment_count': comment_count,

    }
    response = render(request, 'free/free_detail.html', context)

    # 쿠기가 존재하는 경우
    if request.COOKIES.get(str(pk)) is not None:
        cookies = request.COOKIES.get(str(pk))
        cookies_list = cookies.split('|')
        if cookies not in cookies_list:
            response.set_cookie(key=str(pk), value=str(cookie_name), expires=None)
            free.hits += 1
            free.save()
            return response
    # 쿠키가 존재하지 않는 경우
    else:
        response.set_cookie(key=str(pk),  value=str(cookie_name), expires=None)
        free.hits += 1
        free.save()
        return response

    return render(request, 'free/free_detail.html', context)

# 글쓰기 폼으로 가기, 글쓰기
@login_message_required
def free_write_view(request):
    if request.method == "POST":
        form = FreeWriterForm(request.POST, request.FILES)
        user = request.session['email']
        user_email = User.objects.get(email =user)

        print("request.FILES:", request.FILES)
        if form.is_valid():
            free = form.save(commit=False)
            free.writer = user_email

            if request.FILES:
                if 'upload_files' in request.FILES.keys():
                    free.filename = request.FILES['upload_files'].name
            free.save()
            return redirect('free:list')
    else:
        # post 요청이 아닐떄 폼을 만들어 준다.
        form = FreeWriterForm()

    return render(request, 'free/free_write.html', {'form':form})

@login_message_required

def free_edit_view(request, pk):
    free = Free.objects.get(id=pk)

    if request.method == "POST":
        if(free.writer == request.user):
            form = FreeWriterForm(request.POST, instance=free)
            if form.is_valid():
                free = form.save(commit=False)
                free.save()
                messages.success(request, '수정되었습니다.')
                return redirect('/free/'+str(pk))
    else:
        if(free.writer == request.user):
            form = FreeWriterForm(instance=free)
            context ={
                'form': form,
                'edit': '수정하기',
            }
            return render(request, 'free/free_write.html', context)
        else:
            messages.error(request,'본인 게시글이 아닙니다.')
            return redirect('/free/'+str(pk))


@login_message_required
def free_delete_view(request, pk):
    free = Free.objects.get(id=pk)
    if free.writer == request.user:
        free.delete()
        messages.success(request, '삭제되었습니다.')
        return redirect('/free/')
    else:
        messages.error(request, '본인의 게시글이 아닙니다.')
        return redirect('/free/'+str(pk))


@login_message_required
def free_download_view(request, pk):
    free = get_object_or_404(Free, pk=pk)
    url = free.upload_files.url[1:]
    file_url = urllib.parse.unquote(url)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(free.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404



# =============================== 댓글 view ===========================


# 댓글 쓰기
@login_message_required
def comment_write_view(request, pk):
    # 게시판  정보 가져오기
    post = get_object_or_404(Free, id=pk)
    # post 값으로 writer 와 content 값 받아오기
    writer = request.POST.get('writer')
    content = request.POST.get('content')
    # content 가 존재한다면 comment object를 생하고 저장
    if content:
        comment = Comment.objects.create(post=post, content=content, writer=request.user)
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        # json 형식으로 보낼 데이터 값들을 만들기
        data ={
            'writer': writer,
            'content': content,
            'created': '방금전',
            'comment_id': comment.id,
            'comment_count': comment_count,
        }
        # 게시판 유져와 댓글 유져가 같으면 글쓴이로 나타내어주기
        if request.user == post.writer:
            data['self-comment'] = '글쓴이'
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


# 게시글 삭제

@login_message_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Free, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk=comment_id)

    if request.user == target_comment.writer:
        target_comment.deleted = True
        target_comment.save()
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        data ={
            'comment_id': comment_id,
            "comment_count": comment_count
        }
        return  HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='applcation/json')