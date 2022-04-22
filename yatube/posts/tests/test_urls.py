from http import HTTPStatus

from django.conf import settings
from django.test import Client, TestCase

from ..models import Post
from . import test_constants as const
from .factories import create_group_object, create_user_object


class PostsUrlsTest(TestCase):
    """Тестируем urls приложения posts."""

    @classmethod
    def setUpClass(cls):
        """Создаём записи в БД для проверки доступности адресов."""
        super().setUpClass()
        cls.author = create_user_object(const.AUTHOR_USERNAME)
        cls.group = create_group_object()
        cls.post = Post.objects.create(
            author=cls.author,
            text=const.POST_TEXT,
            group=cls.group,
        )
        post_id = cls.post.pk
        cls.POST_DETAILS_URL = f'/posts/{post_id}/'
        cls.POST_EDIT_URL = f'/posts/{post_id}/edit/'

    def setUp(self):
        """Создаём неавторизированный и авторизированный клиенты,
        и клиент автора тестового поста.
        """
        self.author_client = Client()
        self.author_client.force_login(PostsUrlsTest.author)

    def test_page_availability(self):
        """Страницы приложения posts доступны."""
        url_list = {
            const.INDEX_URL: self.client,  # доступна всем
            const.GROUP_LIST_URL: self.client,  # всем
            const.PROFILE_URL: self.client,  # всем
            PostsUrlsTest.POST_DETAILS_URL: self.client,  # всем
            const.POST_CREATE_URL: self.author_client,  # авторизированным
            PostsUrlsTest.POST_EDIT_URL: self.author_client,  # автору
        }
        for url, client in url_list.items():
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_non_existent_page(self):
        """Запрос к несуществующей странице вернёт ошибку 404."""
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_use_correct_templates(self):
        """Страницы приложения posts используют верные шаблоны."""
        urls_and_expected_templates = {
            const.INDEX_URL: settings.INDEX_TEMPLATE,
            const.GROUP_LIST_URL: settings.GROUP_LIST_TEMPLATE,
            const.PROFILE_URL: settings.PROFILE_TEMPLATE,
            PostsUrlsTest.POST_DETAILS_URL: settings.POST_DETAILS_TEMPLATE,
            const.POST_CREATE_URL: settings.POST_CREATE_TEMPLATE,
            PostsUrlsTest.POST_EDIT_URL: settings.POST_CREATE_TEMPLATE,
        }
        for url, template in urls_and_expected_templates.items():
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertTemplateUsed(response, template)
