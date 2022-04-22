from django.utils import timezone as tz


def year(request):
    """Добавляет переменную с текущим годом."""
    current_year = tz.now().year
    return {
        'year': current_year
    }
