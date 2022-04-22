import shutil
import tempfile

from django import forms
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Follow, Post
from . import test_constants as const
from .factories import (create_group_object, create_small_gif,
                        create_user_object)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTest(TestCase):
    """Тестируем views приложения posts."""

    @classmethod
    def setUpClass(cls):
        """Создаём группу для тестирования group_list.
        Создаём пост для тестирования post_details, посты
        для тестирования количества постов автора, которое
        задаётся константой AUTHOR_POST_COUNT.
        Находим URL-адреса для post_details и post_edit.
        """
        super().setUpClass()
        cls.group = create_group_object()
        cls.author = create_user_object(const.AUTHOR_USERNAME)
        # создаём посты для тестированию Paginator
        for _ in range(const.AUTHOR_POST_COUNT - 1):
            Post.objects.create(
                text=const.POST_TEXT,
                author=cls.author,
                group=cls.group,
            )
        # создаём пост для теста Post_details
        cls.POST: Post = Post.objects.create(
            # для теста длина поста должна быть больше заглавия
            text=const.ONE_LETTER_WORD * settings.POST_TITLE_LENGTH * 2,
            author=cls.author,
            group=cls.group,
            image=create_small_gif(),
        )
        cls.POST_ID = cls.POST.pk
        cls.POST_DETAILS_URL = reverse(
            'posts:post_details', kwargs={'post_id': cls.POST_ID}
        )
        cls.POST_EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': cls.POST_ID}
        )

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Авторизируем клиент, как автора тестового поста."""
        self.client.force_login(PostsViewsTest.author)

    def test_pages_use_correct_template(self):
        """URL-адреса приложения posts используют соотвествующие шаблоны."""
        templates_pages_names = {
            const.INDEX_URL: settings.INDEX_TEMPLATE,
            const.GROUP_LIST_URL: settings.GROUP_LIST_TEMPLATE,
            const.PROFILE_URL: settings.PROFILE_TEMPLATE,
            PostsViewsTest.POST_DETAILS_URL: settings.POST_DETAILS_TEMPLATE,
            const.POST_CREATE_URL: settings.POST_CREATE_TEMPLATE,
            PostsViewsTest.POST_EDIT_URL: settings.POST_CREATE_TEMPLATE,
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_details_page_show_correct_context(self):
        """Шаблон post_details сформирован с правильным контекстом."""
        response = self.client.get(PostsViewsTest.POST_DETAILS_URL)
        field_and_expected_context = {
            'post': Post.objects.filter(pk=PostsViewsTest.POST_ID).get(),
            'post_count': const.AUTHOR_POST_COUNT,
            'post_title': const.ONE_LETTER_WORD * settings.POST_TITLE_LENGTH,
        }
        for field_name, expected_context in field_and_expected_context.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    response.context.get(field_name),
                    expected_context
                )

    def test_create_post_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        responses = (
            self.client.get(const.POST_CREATE_URL),
            self.client.get(PostsViewsTest.POST_EDIT_URL),
        )

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }

        for response in responses:
            for field_name, expected in form_fields.items():
                with self.subTest(field=field_name):
                    received_form: PostForm = response.context.get('form')
                    form_field = received_form.fields.get(field_name)
                    self.assertIsInstance(form_field, expected)

        # в форму редактирования попадают значения из нужного поста
        received_form: PostForm = responses[1].context.get('form')
        post_from_received_form: Post = received_form.instance
        received_text = post_from_received_form.text
        received_group = post_from_received_form.group
        self.assertEqual(received_text, self.POST.text)
        self.assertEqual(received_group, self.POST.group)

    def test_index_page_show_correct_context(self):
        """Шаблон index/ group_list/ profile сформирован
        с правильным контекстом.
        """
        urls_expected_posts = (
            (
                const.INDEX_URL,
                Post.objects.latest('pub_date'),
            ),
            (
                const.GROUP_LIST_URL,
                PostsViewsTest.group.posts.latest('pub_date'),
            ),
            (
                const.PROFILE_URL,
                PostsViewsTest.author.posts.latest('pub_date'),
            ),
        )
        for url, expected_post in urls_expected_posts:
            with self.subTest(url=url):
                response = self.client.get(url)
                first_post = response.context['page_obj'][0]
                self.assertEqual(first_post, expected_post)

    def test_first_page_contains_right_amount_records(self):
        """Paginator: страницы содержат верное количество записей."""
        urls = (
            const.INDEX_URL,
            const.GROUP_LIST_URL,
            const.PROFILE_URL,
        )
        for url in urls:
            page_number = 0
            while page_number < 2:
                response = self.client.get(url + '?page=2' * page_number)
                self.assertEqual(
                    len(response.context['page_obj']),
                    (settings.NUMBER_OF_ELEMENTS_PER_PAGE - (
                        2 * settings.NUMBER_OF_ELEMENTS_PER_PAGE - (
                            const.AUTHOR_POST_COUNT)) * page_number))
                page_number += 1

    def test_creating_post(self):
        """Если при создании поста указать группу, то этот пост появится
        - на главной странице
        - на странице группы
        - в профайле пользователя
        """
        self.another_group = create_group_object(
            title=const.ANOTHER_GROUP_TITLE,
            slug=const.ANOTHER_GROUP_SLUG,
            description=const.ANOTHER_GROUP_DESCRIPTION,
        )
        self.ANOTHER_GROUP_URL = reverse(
            'posts:group_list',
            kwargs={'slug': const.ANOTHER_GROUP_SLUG}
        )
        self.created_post = Post.objects.create(
            text=const.EDITED_POST_TEXT,
            group=PostsViewsTest.group,
            author=PostsViewsTest.author,
        )
        urls = (
            const.INDEX_URL,
            const.GROUP_LIST_URL,
            const.PROFILE_URL
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                first_post = response.context['page_obj'][0]
                self.assertEqual(first_post, self.created_post)
        response = self.client.get(self.ANOTHER_GROUP_URL)
        posts_from_another_group = response.context['page_obj']
        self.assertFalse(posts_from_another_group)


class CacheTest(TestCase):
    """Тестирование работы кэширования."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = create_user_object(const.AUTHOR_USERNAME)

    def test_posts_from_index_page_are__cached(self):
        """Посты на главной странице сохраняются в кэш."""
        post: Post = Post.objects.create(
            text=const.POST_TEXT,
            group=None,
            author=CacheTest.author,
        )
        first_response = self.client.get(const.INDEX_URL)
        post.delete()
        response_after_deletion = self.client.get(const.INDEX_URL)
        self.assertEqual(
            first_response.content,
            response_after_deletion.content,
            msg='Пост пропал со страницы после удаления.'
        )


class FollowTest(TestCase):
    """Тест подписок на авторов."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = create_user_object(const.AUTHOR_USERNAME)
        cls.follower = create_user_object(const.TEST_USER_USERNAME)

    def setUp(self) -> None:
        self.follower_client = Client()
        self.follower_client.force_login(FollowTest.follower)
        self.author_client = Client()
        self.author_client.force_login(FollowTest.author)

    def test_authorized_user_can_ubscribe_to_other_users(self):
        """Авторизованный пользователь может подписываться
        на других пользователей и удалять их из подписок.
        """
        follow_count = FollowTest.follower.follower.count()
        self.follower_client.get(const.PROFILE_FOLLOW_URL)
        self.assertEqual(
            FollowTest.follower.follower.count(),
            follow_count + 1,
            msg=('После запроса "подписаться" '
                 'подписка у пользователя не появилась.'),
        )
        self.follower_client.get(const.PROFILE_UNFOLLOW_URL)
        self.assertEqual(
            FollowTest.follower.follower.count(),
            follow_count,
            msg=('После запроса "отписаться"'
                 'подписка у пользователя не исчезла.'),
        )

    def test_new_post_is_shown_to_subscribers(self):
        """Новая запись пользователя появляется в ленте тех,
        кто на него подписан и не появляется в ленте тех, кто не подписан.
        """
        Follow.objects.create(
            author=FollowTest.author,
            user=FollowTest.follower
        )
        post = Post.objects.create(
            text=const.POST_TEXT,
            group=None,
            author=FollowTest.author
        )
        test_params = {
            'follower': {
                'client': self.follower_client,
                'method': self.assertEqual,
                'msg': 'Пост не появился у подписанного пользователя.',
            },
            'author': {
                'client': self.author_client,
                'method': self.assertNotEqual,
                'msg': 'У неподписанного пользователя появился пост.',
            },
        }

        for username, params in test_params.items():
            with self.subTest():
                response = params['client'].get(const.FOLLOW_INDEX_URL)
                try:
                    first_post = response.context.get('page_obj')[0]
                except IndexError:
                    first_post = None
                params['method'](
                    first_post,
                    post,
                    msg=params['msg'],
                )
