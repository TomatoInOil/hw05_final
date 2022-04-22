import shutil
import tempfile

from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Post
from . import test_constants as const
from .factories import create_small_gif, create_user_object

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    """Тест стандартного поведения формы PostForm."""

    @classmethod
    def setUpClass(cls):
        """Создание записи в БД."""
        super().setUpClass()
        cls.author = create_user_object(const.AUTHOR_USERNAME)
        cls.post = Post.objects.create(
            text=const.POST_TEXT,
            group=None,
            author=cls.author,
        )

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Авторизируем в клиенте автора поста."""
        self.client.force_login(PostFormTests.author)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': const.EDITED_POST_TEXT,
            'image': create_small_gif(),
        }
        response = self.client.post(
            const.POST_CREATE_URL,
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, const.PROFILE_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)

        latest_post = Post.objects.latest('pub_date')
        self.assertEqual(latest_post.text, form_data['text'])
        self.assertEqual(latest_post.author, PostFormTests.author)
        self.assertEqual(latest_post.image, const.PATH_TO_SMALL_GIF)

    def test_edit_post(self):
        """При редактировании поста
        изменяется запись в БД с соответсвующим post_id.
        """
        posts_count = Post.objects.count()
        self.POST_ID = PostFormTests.post.pk
        self.POST_DETAILS_URL = reverse(
            'posts:post_details', kwargs={'post_id': self.POST_ID}
        )
        self.POST_EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': self.POST_ID}
        )

        original_text = Post.objects.get(id=self.POST_ID).text
        form_data = {
            'text': const.EDITED_POST_TEXT
        }
        response = self.client.post(
            self.POST_EDIT_URL,
            data=form_data,
            follow=True
        )
        changed_text = Post.objects.get(id=self.POST_ID).text

        self.assertNotEqual(original_text, changed_text)
        self.assertRedirects(response, self.POST_DETAILS_URL)
        self.assertEqual(Post.objects.count(), posts_count)


class CommentFormTest(TestCase):
    """Тестируем работу комментариев."""

    @classmethod
    def setUpClass(cls):
        """Добавляем пост для комментирования.
        Находим ссылку на форму комментирования.
        """
        super().setUpClass()
        cls.author = create_user_object(username=const.AUTHOR_USERNAME)
        cls.POST = Post.objects.create(
            text=const.POST_TEXT,
            group=None,
            author=cls.author
        )
        cls.POST_ID = cls.POST.pk
        cls.ADD_COMMENT_URL = reverse(
            'posts:add_comment', kwargs={'post_id': cls.POST_ID}
        )
        cls.POST_DETAILS_URL = reverse(
            'posts:post_details', kwargs={'post_id': cls.POST_ID}
        )
        cls.LOGIN_REDIRECT_URL = (reverse('users:login') + '?next=' + (
            cls.ADD_COMMENT_URL))

    def setUp(self):
        """Создаём авторизированный клиент."""
        self.user = create_user_object(const.TEST_USER_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_only_authorized_user_can_add_comment(self):
        """Только авторизированный пользователь
        может добавить комментарий.
        """
        users = {
            'authorized': (
                self.authorized_client, CommentFormTest.POST_DETAILS_URL),
            'unauthorized': (
                self.client, CommentFormTest.LOGIN_REDIRECT_URL),
        }
        form_data = {
            'text': const.POST_TEXT
        }

        for user_name, client_and_redirect in users.items():
            with self.subTest(user=user_name):
                response = client_and_redirect[0].post(
                    CommentFormTest.ADD_COMMENT_URL,
                    data=form_data,
                    follow=True,
                )
                self.assertRedirects(response, client_and_redirect[1])

    def test_valid_comment_form_adds_comment_on_post_page(self):
        """После успешной отправки комментарий появляется на странице поста."""
        comment_count = CommentFormTest.POST.comments.count()
        form_data = {
            'text': const.POST_TEXT
        }
        self.authorized_client.post(
            CommentFormTest.ADD_COMMENT_URL,
            data=form_data,
            follow=True,
        )
        self.assertEqual(CommentFormTest.POST.comments.count(), (
            comment_count + 1))

        latest_comment = CommentFormTest.POST.comments.latest('pub_date')
        self.assertEqual(latest_comment.text, form_data['text'])
        self.assertEqual(latest_comment.author, self.user)
