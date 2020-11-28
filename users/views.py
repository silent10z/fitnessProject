from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import generic
from .decorators import *
from .forms import UserRegistreForm, LoginForm, RecoveryEmailForm, CustomPasswordChangeForm, CheckPasswordForm
from .models import User
from django.views.generic import View, CreateView, FormView
from django.contrib import messages
import json
from django.core.serializers.json import DjangoJSONEncoder



# 인덱스로 가는 뷰
class IndexView(generic.TemplateView):

    template_name = "common/index.html"


# 회원가입 뷰
class UserRegisterView(CreateView):

    model = User
    template_name = 'users/user_form.html'
    form_class = UserRegistreForm
    # success_url ="/users/login"
    # success_message = "회원가입 성공."

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "회원가입 성공.")
        return redirect("/users/login")

    def form_valid(self, form):
        self.object = form.save()
        return redirect("/users/login")

# 이용 약관
@method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    # url로 약관을 호출 받을 때
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'users/agreement.html')
    # 받은 post 값으로 회원가입으로 가게 하기
    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True

            if request.POST.get('register') == 'register':
                return redirect('/users/create/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'users/agreement.html')


@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = "users/login_form.html"
    form_class = LoginForm
    success_url = '/users/'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request , email=email, password=password)
        if user is not None:
            self.request.session['email'] = email
            self.request.session['username'] = user.username
            login(self.request, user)

        return super().form_valid(form)
# 로그아웃 뷰
def logout_view(request):
    logout(request)
    return redirect('/users/')


# 아이디 찾기 뷰 작성

@method_decorator(logout_message_required, name='dispatch')
class RecoveryEmailView(View):
    tempalte_name = 'users/recovery_email.html'
    recovery_email = RecoveryEmailForm

    def get(self, request):
        if request.method == "GET":
            form_id = self.recovery_email(None)
        return render(request, self.tempalte_name, {'form': form_id,})

    # ajax 통신으로 바로 확인
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        print('email:{} , username:{}'.format(email, username))
        result_email = User.objects.get(email=email, username=username)
        return HttpResponse(json.dumps({"result_email": result_email.email}, cls=DjangoJSONEncoder), content_type = "application/json")


@login_message_required
def password_edit_view(request):
    if request.method == "POST":
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호를 성공적으로 변경하였습니다.')
            return redirect("users:index")
    elif request.method == "GET":
        print(request.user)
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'users/profile_password.html', {'password_change_form':password_change_form})


@login_message_required
def profile_view(request):
    if request.method == 'GET':
        return render(request, 'users/profile.html')


@login_message_required
def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.info(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/users/login')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'users/profile_delete.html', {'password_form':password_form})
