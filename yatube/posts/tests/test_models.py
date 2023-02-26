import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase, override_settings
from mixer.backend.django import mixer
from testdata import wrap_testdata

from core.utils import cut_string
from posts.models import Group, Post

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

    def setUp(self) -> None:
        cache.clear()

    def test_post_correct_def_str(self) -> None:
        """Проверяем, что у модели post корректно работает __str__."""
        self.assertEqual(cut_string(self.post.text), str(self.post))

    def test_post_correct_verbose_name(self) -> None:
        """verbose_name в полях модели post совпадают с ожидаемыми."""
        field_verboses = {
            'text': 'текст',
            'created': 'дата публикации',
            'author': 'автор',
            'group': 'сообщество',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Post._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_post_correct_help_text(self) -> None:
        """help_text в полях модели post совпадают с ожидаемыми."""
        field_help_texts = {
            'text': 'Введите текст поста',
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
        """Проверяем, что у модели group корректно работает __str__."""
        self.assertEqual(cut_string(self.group.title), str(self.group))

    def test_group_correct_verbose_name(self) -> None:
        """verbose_name в полях модели group совпадают с ожидаемыми."""
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
        """help_text в полях модели group совпадают с ожидаемыми."""
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
