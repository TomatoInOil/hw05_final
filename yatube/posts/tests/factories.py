from django.core.files.uploadedfile import SimpleUploadedFile
from . import test_constants as const
from django.contrib.auth import get_user_model
from ..models import Group

User = get_user_model()


def create_small_gif() -> SimpleUploadedFile:
    """Создает маленькое изображение."""
    uploaded_gif = SimpleUploadedFile(
        name=const.NAME_SMALL_GIF,
        content=const.B_SMALL_GIF,
        content_type=const.CONTENT_TYPE_SMALL_GIF,
    )
    return uploaded_gif


def create_user_object(username) -> User:
    """Создаёт пользователя."""
    return User.objects.create_user(username=username)


def create_group_object(
    title=const.GROUP_TITLE,
    slug=const.GROUP_SLUG,
    description=const.GROUP_DESCRIPTION
) -> Group:
    """Создаёт объект группы."""
    return Group.objects.create(
        title=title,
        slug=slug,
        description=description,
    )
