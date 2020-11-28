from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'gender', 'joined_at', 'last_login_at', 'is_superuser', 'is_active')
    list_display_links = ('id', 'email')
    exclude = ('password',)

    def joined_at(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')

    def last_login_at(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime('%Y-%m-%d %H:%M')

    search_fields = ('id', 'email', 'username', 'gender')
    joined_at.admin_order_field = '-data_joined'
    joined_at.short_description = '가입일'
    last_login_at.admin_order_field = 'las_login_at'
    last_login_at.short_description = '최근로그인'