import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, override_settings
from mixer.backend.django import mixer
from testdata import wrap_testdata

from core.utils import cut_string
from posts.models import Comment, Follow, Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsModelsTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls) -> None:
        cls.post = mixer.blend('posts.Post')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_post_correct_def_str(self) -> None:
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(cut_string(self.post.text), str(self.post))

    def test_post_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Post совпадают с ожидаемыми."""
        field_verboses = {
            'text': 'текст',
            'created': 'дата публикации',
            'author': 'автор',
            'group': 'сообщество',
            'image': 'картинка',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Post._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_post_correct_help_text(self) -> None:
        """help_text в полях модели Post совпадают с ожидаемыми."""
        field_help_texts = {
            'text': 'Введите текст',
            'group': 'Группа, к которой будет относиться пост',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Post._meta.get_field(value).help_text,
                    expected,
                )


class GroupsModelsTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls) -> None:
        cls.group = mixer.blend('posts.Group')

    def test_group_correct_def_str(self) -> None:
        """Проверяем, что у модели Group корректно работает __str__."""
        self.assertEqual(cut_string(self.group.title), str(self.group))

    def test_group_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Group совпадают с ожидаемыми."""
        field_verboses = {
            'title': 'имя',
            'slug': 'адрес',
            'description': 'описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Group._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_group_correct_help_text(self) -> None:
        """help_text в полях модели Group совпадают с ожидаемыми."""
        field_help_texts = {
            'title': 'Введите имя группы',
            'slug': 'Введите адрес группы',
            'description': 'Введите описание группы',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Group._meta.get_field(value).help_text,
                    expected,
                )


class CommentModelsTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls) -> None:
        cls.comment = mixer.blend('posts.Comment')

    def test_comment_correct_def_str(self) -> None:
        """Проверяем, что у модели Comment корректно работает __str__."""
        self.assertEqual(cut_string(self.comment.text), str(self.comment))

    def test_comment_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Comment совпадают с ожидаемыми."""
        field_verboses = {
            'post': 'пост',
            'text': 'текст',
            'created': 'дата публикации',
            'author': 'автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Comment._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_comment_correct_help_text(self) -> None:
        """help_text в полях модели Comment совпадают с ожидаемыми."""
        field_help_texts = {
            'text': 'Введите текст',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Comment._meta.get_field(value).help_text,
                    expected,
                )


class FollowModelsTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls) -> None:
        cls.follow = mixer.blend('posts.Follow')

    def test_follow_correct_def_str(self) -> None:
        """Проверяем, что у модели Follow корректно работает __str__."""
        self.assertEqual(
            f'`{self.follow.user}` подписался на `{self.follow.author}`',
            str(self.follow),
        )

    def test_comment_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Follow совпадают с ожидаемыми."""
        field_verboses = {
            'user': 'пользователь',
            'author': 'автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Follow._meta.get_field(value).verbose_name,
                    expected,
                )
