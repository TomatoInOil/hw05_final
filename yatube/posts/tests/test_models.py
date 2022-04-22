from django.conf import settings
from django.test import TestCase

from ..models import Post
from . import test_constants as const
from .factories import create_group_object, create_user_object


class PostModelTest(TestCase):
    """Тестируем модели приложения posts."""

    @classmethod
    def setUpClass(cls):
        """Создаём тестовые экземпляры моделей Post и Group."""
        super().setUpClass()
        cls.user = create_user_object(const.TEST_USER_USERNAME)
        cls.group = create_group_object()
        cls.post = Post.objects.create(
            author=cls.user,
            text=const.ONE_LETTER_WORD * settings.POST_STR_LENGTH * 2,
        )

    def test_models_have_correct_object_names(self):
        """У моделей приложения posts корректно работает __str__."""
        calls_and_expected_values = {
            'post': (
                PostModelTest.post.__str__(),
                const.ONE_LETTER_WORD * settings.POST_STR_LENGTH
            ),
            'group': (PostModelTest.group.__str__(), const.GROUP_TITLE),
        }
        for model_name, values in calls_and_expected_values.items():
            with self.subTest(model=model_name):
                self.assertEqual(
                    values[0], values[1],
                    (f'Метод __str__ модели {model_name} '
                     'работает некорректно.')
                )
