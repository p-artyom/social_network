import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from mixer.backend.django import mixer
from testdata import wrap_testdata

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PaginatorTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls) -> None:
        cls.author = mixer.blend(User)
        cls.group = mixer.blend('posts.Group')
        cls.posts = mixer.cycle(13).blend(
            'posts.Post',
            author=cls.author,
            group=cls.group,
        )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = Client()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        cache.clear()

    def test_paginator(self) -> None:
        """На страницы передаётся ожидаемое количество объектов."""
        page_names_num_objects = (
            (reverse('posts:index'), settings.NUM_OBJECTS_ON_PAGE),
            (
                reverse(
                    'posts:group_list',
                    kwargs={'slug': self.group.slug},
                ),
                settings.NUM_OBJECTS_ON_PAGE,
            ),
            (
                reverse(
                    'posts:profile',
                    kwargs={'username': self.author},
                ),
                settings.NUM_OBJECTS_ON_PAGE,
            ),
        )
        for page_name, num_object in page_names_num_objects:
            with self.subTest(page_name=page_name, num_object=num_object):
                self.assertEqual(
                    len(self.user.get(page_name).context['page_obj']),
                    num_object,
                )
