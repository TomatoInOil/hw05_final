from http import HTTPStatus

from django.conf import settings
from django.shortcuts import render


def page_not_found(request, exception):
    """Страница ошибки 404 (NOT_FOUND)."""
    return render(
        request,
        template_name=settings.NOT_FOUND_TEMPLATE,
        context={'path': request.path},
        status=HTTPStatus.NOT_FOUND
    )


def csrf_failure(request, reason=''):
    """Страница ошибки 403 (CSRF_FAILURE)."""
    return render(request, settings.CSRF_FAILURE_TEMPLATE)


def permission_denied(request, reason=''):
    """Страница ошибки 403 (PERMISSION DENIED)."""
    return render(request, settings.PERMISSION_DENIED_TEMPLATE)


def server_error(request, exception=None):
    """Страница ошибки 500 (INTERNAL_SERVER_ERROR)."""
    return render(
        request,
        template_name=settings.INTERNAL_SERVER_ERROR,
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )
