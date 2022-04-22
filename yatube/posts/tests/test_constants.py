from django.urls import reverse
from django.conf import settings

POST_TEXT = 'Тестовый текст'
EDITED_POST_TEXT = 'Другой тестовый текст'
ONE_LETTER_WORD = 'т'

GROUP_TITLE = 'Тестовая группа'
GROUP_SLUG = 'test-slug'
GROUP_DESCRIPTION = 'Тестовое описание'
ANOTHER_GROUP_TITLE = 'Другая группа'
ANOTHER_GROUP_SLUG = 'another-slug'
ANOTHER_GROUP_DESCRIPTION = 'Описание другой группы'

AUTHOR_USERNAME = 'testauthor'
PROFILE_URL = reverse('posts:profile', kwargs={'username': AUTHOR_USERNAME})
PROFILE_FOLLOW_URL = reverse(
    'posts:profile_follow', kwargs={'username': AUTHOR_USERNAME}
)
PROFILE_UNFOLLOW_URL = reverse(
    'posts:profile_unfollow', kwargs={'username': AUTHOR_USERNAME}
)

TEST_USER_USERNAME = 'testuser'

AUTHOR_POST_COUNT = int(settings.NUMBER_OF_ELEMENTS_PER_PAGE * 1.5)

INDEX_URL = reverse('posts:index')
FOLLOW_INDEX_URL = reverse('posts:follow_index')
GROUP_LIST_URL = reverse('posts:group_list', kwargs={'slug': GROUP_SLUG})
POST_CREATE_URL = reverse('posts:post_create')

B_SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
NAME_SMALL_GIF = 'small.gif'
CONTENT_TYPE_SMALL_GIF = 'image/gif'
PATH_TO_SMALL_GIF = settings.POST_IMAGE_UPLOAD_TO + NAME_SMALL_GIF
