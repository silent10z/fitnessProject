import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from uuid import uuid4
from datetime import datetime, timedelta


# 암호화 시키기
def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file/', ymd_path, uuid_name])

class Free(models.Model):

    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    title = models.CharField(max_length=128, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    hits = models.PositiveIntegerField(verbose_name="조회수", default=0)
    registered_date = models.DateTimeField(verbose_name='등록시간', default=timezone.now)
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    ## PositiveIntegerField 양수만을 받아줌
    comments = models.PositiveIntegerField(verbose_name='댓글수', null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'free_board'
        verbose_name = '자유게시판'
        verbose_name_plural = '자유게시판'

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.registered_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.registered_date.date()
            return str(time.days) + '일 전'
        else:
            return False


class Comment(models.Model):
    post = models.ForeignKey(Free, on_delete=models.CASCADE, verbose_name='게시글')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='댓글작성자')
    content = models.TextField(verbose_name='댓글내용')
    created = models.DateTimeField(verbose_name="작성일", default=timezone.now)
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'free_board_comment'
        verbose_name = '자유게시판 댓글'
        verbose_name_plural = '자유게시판 댓글'

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(time.days) + '일 전'
        else:
            return False
