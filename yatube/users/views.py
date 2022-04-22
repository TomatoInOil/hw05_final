from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    """Класс для рендера страницы регистрации."""

    form_class = CreationForm
    template_name = 'users/signup.html'

    def get_success_url(self) -> str:
        return reverse_lazy('posts:index')
