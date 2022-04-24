from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .factories import create_page_obj
from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def index(request):
    """Рендер главной страницы сайта,
    где расположены 10 последних обновлений.
    """
    template = settings.INDEX_TEMPLATE

    post_list = Post.objects.select_related('group', 'author').all()
    page_obj = create_page_obj(post_list, request)

    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Рендер страницы группы,
    на которой выводятся 10 последних обновлений,
    отфильтрованных по группе.
    """
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author').all()
    page_obj = create_page_obj(post_list, request)

    template = settings.GROUP_LIST_TEMPLATE
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """Рендер страницы профайла пользователя."""
    template = settings.PROFILE_TEMPLATE

    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group',).all()
    page_obj = create_page_obj(post_list, request)

    following = False
    if request.user.is_authenticated:
        following = request.user.follower.filter(author=author).exists()

    context = {
        'page_obj': page_obj,
        'author': author,
        'following': following,
    }
    return render(request, template, context)


def post_details(request, post_id):
    """Рендер страницы отдельного поста."""
    post = get_object_or_404(
        Post.objects.select_related('group', 'author'), pk=post_id
    )

    comments_list = post.comments.select_related('author').all()
    page_obj = create_page_obj(comments_list, request)

    template = settings.POST_DETAILS_TEMPLATE
    context = {
        'post': post,
        'post_title': post.text[:settings.POST_TITLE_LENGTH],
        'form': CommentForm(),
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Рендер страницы создания новой записи."""
    template = settings.POST_CREATE_TEMPLATE

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        post = form.save(commit=False)
        author = request.user
        post.author_id = author.id
        post.save()
        return redirect('posts:profile', author.username)
    action_url = reverse('posts:post_create')
    context = {
        'form': form,
        'is_edit': False,
        'action_url': action_url,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """Рендер страницы редактирования записи."""
    template = settings.POST_CREATE_TEMPLATE
    redirect_details = redirect('posts:post_details', post_id)

    post = get_object_or_404(Post, pk=post_id)
    if request.user.id != post.author.id:
        return redirect_details

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if not form.is_valid():
        action_url = reverse('posts:post_edit', kwargs={'post_id': post_id})
        context = {
            'form': form,
            'is_edit': True,
            'post_id': post_id,
            'action_url': action_url
        }
        return render(request, template, context)

    form.save()
    return redirect_details


@login_required
def add_comment(request, post_id):
    """Обработка отправленного комментария."""
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = Post.objects.get(id=post_id)
        comment.save()
    return redirect('posts:post_details', post_id=post_id)


@login_required
def follow_index(request):
    """Отображение страницы с постами,
    на авторов которых подписан пользователь.
    """
    subscriptions = request.user.follower.all()
    post_list = Post.objects.filter(author__following__in=subscriptions)
    page_obj = create_page_obj(post_list, request)

    context = {
        'page_obj': page_obj,
    }
    return render(request, settings.FOLLOW_TEMPLATE, context)


@login_required
def profile_follow(request, username):
    """Подписка на автора."""
    follower = request.user
    following = get_object_or_404(User, username=username)
    try:
        Follow.objects.create(
            author=following,
            user=follower,
        )
    except IntegrityError:
        return HttpResponseForbidden()
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    """Отписка от автора."""
    follower = request.user
    following = get_object_or_404(User, username=username)
    follow = get_object_or_404(Follow, author=following, user=follower)
    follow.delete()
    return redirect('posts:profile', username)
