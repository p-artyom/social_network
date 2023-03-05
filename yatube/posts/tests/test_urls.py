import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from mixer.backend.django import mixer
from testdata import wrap_testdata

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsUrlsTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls) -> None:
        cls.user, cls.author = mixer.cycle(2).blend(User)
        cls.group = mixer.blend('posts.Group')
        cls.post = mixer.blend(
            'posts.Post',
            author=cls.author,
            group=cls.group,
        )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = Client()
        cls.author_user = Client()

        cls.authorized_user.force_login(cls.user)
        cls.author_user.force_login(cls.author)

        cls.urls = {
            'group': reverse(
                'posts:group_list',
                kwargs={'slug': cls.group.slug},
            ),
            'index': reverse('posts:index'),
            'profile': reverse(
                'posts:profile',
                kwargs={'username': cls.post.author},
            ),
            'post_edit': reverse(
                'posts:post_edit',
                kwargs={'pk': cls.post.id},
            ),
            'post_detail': reverse(
                'posts:post_detail',
                kwargs={'pk': cls.post.id},
            ),
            'post_create': reverse('posts:post_create'),
            'unexisting_page': '/unexisting_page/',
            'post_comment': reverse(
                'posts:add_comment',
                kwargs={'pk': cls.post.id},
            ),
            'follow': reverse('posts:follow_index'),
            'profile_follow': reverse(
                'posts:profile_follow',
                kwargs={'username': cls.post.author},
            ),
            'profile_unfollow': reverse(
                'posts:profile_unfollow',
                kwargs={'username': cls.post.author},
            ),
        }

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_http_statuses(self) -> None:
        """URL-адрес возвращает соответствующий статус."""
        httpstatuses = (
            (self.urls.get('group'), HTTPStatus.OK, self.client),
            (self.urls.get('index'), HTTPStatus.OK, self.client),
            (self.urls.get('profile'), HTTPStatus.OK, self.client),
            (self.urls.get('post_detail'), HTTPStatus.OK, self.client),
            (
                self.urls.get('unexisting_page'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (self.urls.get('post_edit'), HTTPStatus.FOUND, self.client),
            (self.urls.get('post_edit'), HTTPStatus.OK, self.author_user),
            (
                self.urls.get('post_edit'),
                HTTPStatus.FOUND,
                self.authorized_user,
            ),
            (self.urls.get('post_create'), HTTPStatus.FOUND, self.client),
            (self.urls.get('post_create'), HTTPStatus.OK, self.author_user),
            (
                self.urls.get('post_create'),
                HTTPStatus.OK,
                self.authorized_user,
            ),
            (
                self.urls.get('post_comment'),
                HTTPStatus.FOUND,
                self.client,
            ),
            (
                self.urls.get('post_comment'),
                HTTPStatus.FOUND,
                self.authorized_user,
            ),
            (
                self.urls.get('follow'),
                HTTPStatus.FOUND,
                self.client,
            ),
            (
                self.urls.get('follow'),
                HTTPStatus.OK,
                self.authorized_user,
            ),
            (
                self.urls.get('profile_follow'),
                HTTPStatus.FOUND,
                self.client,
            ),
            (
                self.urls.get('profile_follow'),
                HTTPStatus.FOUND,
                self.authorized_user,
            ),
            (
                self.urls.get('profile_unfollow'),
                HTTPStatus.FOUND,
                self.client,
            ),
            (
                self.urls.get('profile_unfollow'),
                HTTPStatus.FOUND,
                self.authorized_user,
            ),
        )
        for url, status, user in httpstatuses:
            with self.subTest(
                url=url,
                status=status,
                user=get_user(user).username,
            ):
                self.assertEqual(user.get(url).status_code, status)

    def test_templates(self) -> None:
        """URL-адрес использует соответствующий шаблон."""
        cache.clear()
        templates = (
            (self.urls.get('index'), 'posts/index.html', self.client),
            (self.urls.get('group'), 'posts/group_list.html', self.client),
            (self.urls.get('profile'), 'posts/profile.html', self.client),
            (
                self.urls.get('post_detail'),
                'posts/post_detail.html',
                self.client,
            ),
            (
                self.urls.get('post_edit'),
                'posts/create_post.html',
                self.author_user,
            ),
            (
                self.urls.get('post_create'),
                'posts/create_post.html',
                self.authorized_user,
            ),
            (
                self.urls.get('unexisting_page'),
                'core/404.html',
                self.client,
            ),
            (
                self.urls.get('follow'),
                'posts/follow.html',
                self.authorized_user,
            ),
        )
        for url, template, user in templates:
            with self.subTest(
                url=url,
                template=template,
                user=get_user(user).username,
            ):
                self.assertTemplateUsed(user.get(url), template)

    def test_redirects(self) -> None:
        """URL-адрес перенаправит на соответствующую страницу."""
        redirects = (
            (
                self.urls.get('post_create'),
                reverse('login') + '?next=' + self.urls.get('post_create'),
                self.client,
            ),
            (
                self.urls.get('post_edit'),
                reverse('login') + '?next=' + self.urls.get('post_edit'),
                self.client,
            ),
            (
                self.urls.get('post_edit'),
                self.urls.get('post_detail'),
                self.authorized_user,
            ),
            (
                self.urls.get('post_comment'),
                self.urls.get('post_detail'),
                self.authorized_user,
            ),
            (
                self.urls.get('profile_follow'),
                self.urls.get('profile'),
                self.authorized_user,
            ),
            (
                self.urls.get('profile_unfollow'),
                self.urls.get('profile'),
                self.authorized_user,
            ),
        )
        for url, forward, user in redirects:
            with self.subTest(
                url=url,
                forward=forward,
                user=get_user(user).username,
            ):
                self.assertRedirects(user.get(url, follow=True), forward)
