from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()

LOGOUT_URL = '/auth/logout/'
SIGNUP_URL = '/auth/signup/'
LOGIN_URL = '/auth/login/'
PASSWORD_RESET_FORM_URL = '/auth/password_reset/'
PASSWORD_RESET_DONE_URL = '/auth/password_reset/done/'
PASSWORD_RESET_COMPLETE_URL = '/auth/password_reset/complete/'
PASSWORD_RESET_CONFIRM_URL = '/auth/password_reset/confirm/<uidb64>/<token>/'
PASSWORD_CHANGE_FORM_URL = '/auth/password_change/'
PASSWORD_CHANGE_DONE_URL = '/auth/password_change/done/'


class UsersUrlTest(TestCase):
    """Тестируем urls приложения users."""

    def setUp(self):
        """Создаём неавторизированный и авторизированный клиенты."""
        self.user = User.objects.create(username='testuser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_page_availability(self):
        """Страницы приложения users доступны."""
        url_list = {
            SIGNUP_URL: self.client,  # доступна всем
            LOGIN_URL: self.client,  # всем
            PASSWORD_RESET_FORM_URL: self.client,  # всем
            PASSWORD_RESET_DONE_URL: self.client,  # всем
            PASSWORD_RESET_COMPLETE_URL: self.client,  # всем
            PASSWORD_RESET_CONFIRM_URL: self.client,  # всем
            PASSWORD_CHANGE_FORM_URL: self.authorized_client,  # авториз.
            PASSWORD_CHANGE_DONE_URL: self.authorized_client,  # авториз.
            # проверка logout разлогинивает клиент, поэтому она последняя
            LOGOUT_URL: self.authorized_client,  # авторизированным
        }
        for url, client in url_list.items():
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_use_correct_templates(self):
        """Страницы приложения users используют верные шаблоны."""
        urls_and_expected_templates = {
            SIGNUP_URL: 'users/signup.html',
            LOGIN_URL: 'users/login.html',
            PASSWORD_RESET_FORM_URL: 'users/password_reset_form.html',
            PASSWORD_RESET_DONE_URL: 'users/password_reset_done.html',
            PASSWORD_RESET_COMPLETE_URL: 'users/password_reset_complete.html',
            PASSWORD_RESET_CONFIRM_URL: 'users/password_reset_confirm.html',
            PASSWORD_CHANGE_FORM_URL: 'users/password_change_form.html',
            PASSWORD_CHANGE_DONE_URL: 'users/password_change_done.html',
            # проверка logout разлогинивает клиент, поэтому она последняя
            LOGOUT_URL: 'users/logged_out.html',
        }
        for url, template in urls_and_expected_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url, follow=True)
                self.assertTemplateUsed(response, template)
