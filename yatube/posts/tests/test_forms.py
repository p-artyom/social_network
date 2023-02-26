import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from mixer.backend.django import mixer
from testdata import wrap_testdata

from posts.models import Comment, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
ZERO_OBJECT = 0
ONE_OBJECT = 1


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFormsTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls) -> None:
        cls.author, cls.not_author = mixer.cycle(2).blend(User)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = Client()
        cls.authorized_user = Client()

        cls.user.force_login(cls.author)
        cls.authorized_user.force_login(cls.not_author)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        cache.clear()

    def test_author_can_create_post(self) -> None:
        """Авторизованный пользователь может создать пост."""
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
        self.group = mixer.blend('posts.Group')
        data = {
            'text': 'Hello, wolrd! Hello, Django!',
            'author': self.author,
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.user.post(
            reverse('posts:post_create'),
            data=data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.author}),
        )
        self.assertEqual(Post.objects.count(), ONE_OBJECT)
        post = Post.objects.get()
        self.assertEqual(post.text, data['text'])
        self.assertEqual(post.author, data['author'])
        self.assertEqual(post.group.id, data['group'])
        self.assertEqual(post.image, 'posts/small.gif')

    def test_anon_can_not_create_post(self) -> None:
        """Анонимный пользователь не может создать пост."""
        data = {
            'text': 'Hello, wolrd! Hello, Django!',
            'author': self.author,
        }
        self.client.post(
            reverse('posts:post_create'),
            data=data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), ZERO_OBJECT)

    def test_author_can_edit_post(self) -> None:
        """Автор может отредактировать свой пост."""
        self.group = mixer.blend('posts.Group')
        self.post = mixer.blend(
            'posts.Post',
            author=self.author,
            group=self.group,
        )
        data = {
            'text': 'Изменяем текст поста!',
            'group': self.group.id,
        }
        response = self.user.post(
            reverse('posts:post_edit', kwargs={'pk': self.post.id}),
            data=data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'pk': self.post.id}),
        )
        post = Post.objects.get()
        self.assertEqual(post.text, data['text'])
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.group.id, data['group'])

    def test_anon_can_not_edit_post(self) -> None:
        """Анонимный пользователь не может редактировать пост."""
        self.group = mixer.blend('posts.Group')
        self.post = mixer.blend(
            'posts.Post',
            author=self.author,
            group=self.group,
        )
        data = {
            'text': 'Изменяем текст поста!',
            'group': self.group.id,
        }
        self.client.post(
            reverse(
                'posts:post_edit',
                kwargs={'pk': self.post.id},
            ),
            data=data,
            follow=True,
        )
        post = Post.objects.get()
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group.id, self.group.id)

    def test_not_author_can_not_edit_post(self) -> None:
        """Не автор поста не может редактировать пост."""
        self.group = mixer.blend('posts.Group')
        self.post = mixer.blend(
            'posts.Post',
            author=self.author,
            group=self.group,
        )
        data = {
            'text': 'Изменяем текст поста!',
            'group': self.group.id,
        }
        response = self.authorized_user.post(
            reverse(
                'posts:post_edit',
                kwargs={'pk': self.post.id},
            ),
            data=data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'pk': self.post.id}),
        )
        post = Post.objects.get()
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group.id, self.group.id)

    def test_create_comment(self) -> None:
        """Комментарий появляется на странице поста."""
        self.post = mixer.blend(
            'posts.Post',
            author=self.author,
        )
        data = {
            'post': self.post,
            'author': self.author,
            'text': 'Первый комментарий!',
        }
        response = self.user.post(
            reverse('posts:add_comment', kwargs={'pk': self.post.id}),
            data=data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'pk': self.post.id}),
        )
        self.assertEqual(Comment.objects.count(), ONE_OBJECT)
        comment = Comment.objects.get()
        self.assertEqual(comment.post, data['post'])
        self.assertEqual(comment.author, data['author'])
        self.assertEqual(comment.text, data['text'])

    def test_anon_can_not_create_comment(self) -> None:
        """Анонимный пользователь не может комментировать пост."""
        self.post = mixer.blend(
            'posts.Post',
            author=self.author,
        )
        data = {
            'post': self.post,
            'author': self.author,
            'text': 'Первый комментарий!',
        }
        self.client.post(
            reverse('posts:add_comment', kwargs={'pk': self.post.id}),
            data=data,
            follow=True,
        )
        self.assertEqual(Comment.objects.count(), ZERO_OBJECT)
