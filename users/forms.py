from django import forms
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm



# 회원 가입 폼
class UserRegistreForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'username', 'hp', 'gender']

    def hp_vaildator(value):
        if len(str(value)) != 10:
            raise forms.ValidationError("정확한 핸드폰 번호를 입력해주십시오.")

# 로그인 폼
class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',}
        ),
        error_messages={'required': '아이디를 입력해주세요.'},
        max_length=35,
        label='이메일'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',}
        ),
        error_messages={'required': '비밀번호를 입력해주세요'},
        label="비밀번호"
    )

    def clean(self):
        # Form 에 있는 clean()을 상속받아 clean_data 를 리턴해온다.
        clean_data = super().clean()
        email = clean_data.get('email')
        password = clean_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.add_error('email', '이메일이 존재하지 않습니다.')
                return
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렷습니다.')

# 아이디 찾기 구현

class RecoveryEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, )
    username = forms.CharField(widget=forms.TextInput,)


    class Meta:
        fields = ['email', 'username']

    def __init__(self, *args, **kwargs):
        super(RecoveryEmailForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '이름'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_username',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_email'
        })


# 비밀번호 변경 구현



class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = "기존 비밀번호"
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = "새 비밀번호"
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = "새 비밀번호 확인"
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })

# 회원 탈퇴 forms

class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control',},
    ))
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')