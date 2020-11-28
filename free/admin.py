from django.contrib import admin
from .models import Free, Comment

@admin.register(Free)
class FreeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'writer',
        'hits',
        'registered_date'
    )
    search_fields = ('title', 'content', 'writer__user_email',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'content',
        'writer',
        'created',
        'deleted',
    )
    search_fields = ('post_title', 'content', 'writer_email')

