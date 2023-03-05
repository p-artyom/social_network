from django.contrib import admin

from core.admin import BaseAdmin
from posts.models import Comment, Follow, Group, Post


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


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    list_display = ('pk', 'post', 'author', 'text')
    search_fields = ('text',)


@admin.register(Follow)
class FollowAdmin(BaseAdmin):
    list_display = ('pk', Follow.__str__)
    search_fields = ('user',)
