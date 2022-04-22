from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):
    """Класс формы для создания нового поста."""

    class Meta():
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(ModelForm):
    """Класс формы для написания комментария к посту."""

    class Meta():
        model = Comment
        fields = ('text',)
