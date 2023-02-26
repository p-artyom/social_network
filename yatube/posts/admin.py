from django.contrib import admin

from core.admin import BaseAdmin
from posts.models import Group, Post


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('pk', 'text', 'created', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('created',)


@admin.register(Group)
class GroupAdmin(BaseAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('slug',)
