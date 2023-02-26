from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from posts import views

app_name = '%(app_label)s'

urlpatterns = [
    path(
        '',
        views.index,
        name='index',
    ),
    path(
        'group/<slug:slug>/',
        views.group_posts,
        name='group_list',
    ),
    path(
        'profile/<str:username>/',
        views.profile,
        name='profile',
    ),
    path(
        'posts/<int:pk>/',
        views.post_detail,
        name='post_detail',
    ),
    path(
        'create/',
        views.post_create,
        name='post_create',
    ),
    path(
        'posts/<int:pk>/edit/',
        views.post_edit,
        name='post_edit',
    ),
    path(
        'posts/<int:pk>/comment/',
        views.add_comment,
        name='add_comment',
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
