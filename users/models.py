from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    GENDER_CHOICES =(
        ("M","남자"),
        ("F", "여자"),
        ("선택안함", "선택안함"),

    )

    email = models.EmailField(max_length=254, verbose_name="이메일", unique=True)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    hp = models.IntegerField(verbose_name="핸드폰번호", null=True, unique=True)
    username = models.CharField(max_length=30, verbose_name="이름", blank=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=30)
    auth = models.CharField(max_length=10, verbose_name="인증번호", null=True)
    is_staff = models.BooleanField(verbose_name='스테프',
                                   default=False,
    )
    is_active = models.BooleanField(verbose_name='할동중',
                                    default=True,
    )

    date_joined = models.DateTimeField('가입일', default=timezone.now)

    USERNAME_FIELD = 'email'   # email을 사용자의 식별자로 설정
    REQUIRED_FIELDS = ['username'] # 필수입력 값

    class Meta:
        # 사용자가 읽기 쉬운 객체으 ㅣ이름으로 관리자 화면에서 표시
        verbose_name = "사용자"
        # verbose_name 의 복수형
        verbose_name_plural = "사용자"
        swappable = 'AUTH_USER_MODEL'
        db_table = "users"

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)