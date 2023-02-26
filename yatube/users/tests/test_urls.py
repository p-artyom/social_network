from http import HTTPStatus

from django.test import TestCase


class StaticPagesURLTests(TestCase):
    def test_url_exists_at_desired_location(self) -> None:
        """Проверка доступности URL-адреса."""
        url_status = {
            '/auth/logout/': HTTPStatus.OK,
            '/auth/signup/': HTTPStatus.OK,
            '/auth/login/': HTTPStatus.OK,
        }
        for url, status in url_status.items():
            with self.subTest(url=url):
                self.assertEqual(
                    self.client.get(url).status_code,
                    status,
                )

    def test_url_uses_correct_template(self) -> None:
        """Проверка шаблона URL-адреса."""
        url_names_templates = {
            '/auth/logout/': 'users/logged_out.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
        }
        for url, template in url_names_templates.items():
            with self.subTest(url=url):
                self.assertTemplateUsed(
                    self.client.get(url),
                    template,
                )
