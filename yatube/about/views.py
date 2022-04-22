from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Класс для рендера страницы об авторе."""

    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Класс для рендера страницы об используемых технологиях."""

    template_name = 'about/tech.html'
