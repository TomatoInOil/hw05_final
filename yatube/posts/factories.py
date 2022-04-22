from typing import Optional

from django.conf import settings
from django.core.paginator import Page, Paginator
from django.db.models.query import QuerySet
from django.http import HttpRequest


def create_page_obj(
    elements_list: QuerySet,
    request: HttpRequest
) -> Page:
    """Функция, создаёт объект страницы и возвращает его,
    получая на вход элементы из БД и запрос.
    """
    paginator: Paginator = Paginator(
        elements_list, settings.NUMBER_OF_ELEMENTS_PER_PAGE
    )
    page_number: Optional[str] = request.GET.get('page')
    page_obj: Page = paginator.get_page(page_number)
    return page_obj
