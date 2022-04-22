from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

ABOUT_AUTHOR_URL = '/about/author/'
ABOUT_TECH_URL = '/about/tech/'


class TestAboutUrls(TestCase):
    """Тестируем urls приложения about."""

    def test_page_availability(self):
        """Страницы приложения about доступны."""
        url_list = (
            ABOUT_AUTHOR_URL,
            ABOUT_TECH_URL,
        )
        for url in url_list:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_use_correct_templates(self):
        """Страницы приложения about используют верные шаблоны."""
        urls_and_expected_templates = {
            ABOUT_AUTHOR_URL: 'about/author.html',
            ABOUT_TECH_URL: 'about/tech.html',
        }
        for url, template in urls_and_expected_templates.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)
