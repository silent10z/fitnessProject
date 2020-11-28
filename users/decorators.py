from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .models import User
from django.http import HttpResponse



# 각 앱마다 사용권한, 을 주기위해서 Decorator 기능을 사용한다.

# 로그인 확인
def login_message_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, '로그인을 하시면 이용가능 합니다.')
            return redirect(settings.LOGIN_URL)
        return function(request, *args, **kwargs)
    return wrap

# 관리자 확인
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.level == '1' or request.user.level == '0':
            return function(request, *args, **kwargs)
        messages.info(request, '접근 권한이 없습니다.')
        return redirect('/users/')
    return  wrap

# 비로그인 확인
def logout_message_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "접속중인 사용자입니다.")
            return redirect('/users/')
        return function(request, *args, **kwargs)
    return wrap


# 사용 방법

# from django.contrib.auth.decorators import login_required 기본 제공

# from users.decorators import *
#
# @login_message_required
# def example_def(request):
#     pass

# from users.decorators import *
# from django.utils.decorators import method_decorator
#
# @method_decorator(logout_message_required, name='dispatch')
# class ExampleClass(View):
#     pass