from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройка административной панели для управления постами."""

    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
        'get_html_image',
    )
    list_display_links = (
        'pk',
        'text',
    )
    list_select_related = ('author', 'group',)  # я правильно понимаю,
    # что это уменьшит в данном случае кол-во запросов к БД?
    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('group',)
    empty_value_display = '-пусто-'

    def view_on_site(self, obj):
        url = reverse('posts:post_details', kwargs={'post_id': obj.pk})
        return url

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f'<img src="{object.image.url}" height=30>')

    get_html_image.short_description = 'Картинка'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Настройка административной панели для управления подписками."""

    list_display = (
        'pk',
        'user',
        'author',
    )
    search_fields = (
        'user__username__startswith',
        'author__username__startswith',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка административной панели для управления комментариями."""

    list_display = (
        'pk',
        'text',
        'post',
        'author',
    )
    list_display_links = (
        'pk',
        'text',
    )
    list_select_related = ('post', 'author',)
    search_fields = (
        'post__text',
        'text',
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Настройка административной панели для управления сообществами."""

    list_display = (
        'pk',
        'title',
        'slug',
        'description',
    )
    list_display_links = (
        'pk',
        'title',
    )

    def view_on_site(self, obj):
        url = reverse('posts:group_list', kwargs={'slug': obj.slug})
        return url
