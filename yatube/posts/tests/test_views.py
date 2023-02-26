import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from mixer.backend.django import mixer
from testdata import wrap_testdata

from posts.models import Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls) -> None:
        cls.user, cls.author = mixer.cycle(2).blend(User)
        cls.group = mixer.blend('posts.Group')
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif',
        )
        cls.post = mixer.blend(
            'posts.Post',
            author=cls.author,
            group=cls.group,
            image=uploaded,
        )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = Client()
        cls.author_user = Client()

        cls.authorized_user.force_login(cls.user)
        cls.author_user.force_login(cls.author)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        cache.clear()

    def test_index_page_show_correct_context(self) -> None:
        """Шаблон index сформирован с правильным контекстом."""
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(
            list(response.context['page_obj']),
            list(Post.objects.select_related('author')),
        )

    def test_group_list_page_show_correct_context(self) -> None:
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        )
        self.assertEqual(
            list(response.context['page_obj']),
            list(Post.objects.select_related('author', 'group')),
        )

    def test_profile_page_show_correct_context(self) -> None:
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author},
            ),
        )
        self.assertEqual(
            list(response.context['page_obj']),
            list(Post.objects.select_related('author')),
        )

    def test_post_detail_page_show_correct_context(self) -> None:
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'pk': self.post.id}),
        )
        self.assertEqual(
            response.context['posts'],
            self.post,
        )

    def test_post_edit_page_show_correct_context(self) -> None:
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.author_user.get(
            reverse('posts:post_edit', kwargs={'pk': self.post.id}),
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value, expected=expected):
                self.assertIsInstance(
                    response.context.get('form').fields.get(value),
                    expected,
                )

    def test_post_create_page_show_correct_context(self) -> None:
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.author_user.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value, expected=expected):
                self.assertIsInstance(
                    response.context.get('form').fields.get(value),
                    expected,
                )

    def test_created_post_present_on_all_pages(self) -> None:
        """Пост, после создания, появляется на главной,
        на странице группы и в профайле пользователя.
        """
        self.post = mixer.blend(
            'posts.Post',
            author=self.post.author,
            group=self.group,
        )
        page_names_posts = {
            reverse('posts:index'): list(
                Post.objects.select_related('author'),
            ),
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug},
            ): list(Post.objects.select_related('author', 'group')),
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author},
            ): list(Post.objects.select_related('author')),
        }
        for page_names, posts in page_names_posts.items():
            with self.subTest(page_names=page_names, posts=posts):
                self.assertEqual(
                    posts,
                    list(
                        self.client.get(page_names).context['page_obj'],
                    ),
                )

    def test_post_not_in_foreign_group(self) -> None:
        """Пост не попал в группу, для которой не был предназначен."""
        group = mixer.blend('posts.Group')
        self.post = mixer.blend(
            'posts.Post',
            author=self.post.author,
            group=group,
        )
        response = self.authorized_user.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        )
        self.assertNotIn(
            Post.objects.exclude(group=group),
            response.context['page_obj'],
        )

    def test_cache(self) -> None:
        """Тестирование кэша"""
        posts = self.author_user.get(reverse('posts:index')).content
        self.post = mixer.blend(
            'posts.Post',
            author=self.post.author,
        )
        self.assertEqual(
            self.author_user.get(reverse('posts:index')).content,
            posts,
        )
        cache.clear()
        self.assertNotEqual(
            self.author_user.get(reverse('posts:index')).content,
            posts,
        )
