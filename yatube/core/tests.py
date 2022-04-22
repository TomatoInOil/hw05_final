from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CoreViewsTest(TestCase):
    """Тестируем views приложения core."""

    def test_not_found_error_page_uses_correct_template(self):
        """Страница ошибки 404 (NOT_FOUND) использует правильный шаблон."""
        response = self.client.get('/non-exist-page/')
        self.assertTemplateUsed(response, settings.NOT_FOUND_TEMPLATE)
