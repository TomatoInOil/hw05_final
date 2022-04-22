from core.models import PubDateModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Модель группы, к которой могут принадлежать публикации."""

    title = models.CharField(
        'Заголовок группы',
        max_length=200,
    )
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(
        'Описание группы',
    )

    def __str__(self):
        return self.title


class Post(PubDateModel):
    """Модель публикации на сайте."""

    text = models.TextField(
        'Текст записи',
        help_text='Это поле для текста Вашей записи полностью принадлежит Вам',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост',
    )
    image = models.ImageField(
        'Картинка',
        upload_to=settings.POST_IMAGE_UPLOAD_TO,
        blank=True,
        help_text=('Вы можете прикрепить картинку к вашему посту. '
                   'Рекомендуемый размер картинки: 960x339'),
    )

    def __str__(self) -> str:
        return self.text[:settings.POST_STR_LENGTH]


class Comment(PubDateModel):
    """Модель комментария под постом."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Расскажите, что вы думаете насчёт данного поста',
    )

    def __str__(self) -> str:
        return self.text[:settings.COMMENT_STR_LENGTH]


class Follow(models.Model):
    """Модель подписок на авторов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор постов',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Верный читатель',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='excluding_duplicate_subscriptions'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='not_the_author'
            ),
        ]

    def __str__(self) -> str:
        follower_username = self.user.username
        following_username = self.author.username
        text = (f'{follower_username} подписан на {following_username}')
        return text
