from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        '',
        include('posts.urls', namespace=apps.get_app_config('posts').name),
    ),
    path(
        'about/',
        include('about.urls', namespace=apps.get_app_config('about').name),
    ),
    path(
        'admin/',
        admin.site.urls,
    ),
    path(
        'auth/',
        include('users.urls', namespace=apps.get_app_config('users').name),
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls'),
    ),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
