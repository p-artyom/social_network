from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from core.utils import paginate
from posts.forms import CommentForm, PostForm
from posts.models import Follow, Group, Post, User


@cache_page(settings.CACHE_TIMEOUT, key_prefix='index_page')
def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'posts/index.html',
        {
            'page_obj': paginate(
                request,
                Post.objects.select_related('author'),
            ),
        },
    )


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    return render(
        request,
        'posts/group_list.html',
        {
            'page_obj': paginate(
                request,
                group.posts.select_related('author', 'group'),
            ),
            'group': group,
        },
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    users = get_object_or_404(User, username=username)
    following = (
        request.user.is_authenticated
        and users.following.filter(user=request.user).exists()
    )
    return render(
        request,
        'posts/profile.html',
        {
            'page_obj': paginate(
                request,
                users.posts.select_related('author'),
            ),
            'users': users,
            'following': following,
        },
    )


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    posts = get_object_or_404(Post, pk=pk)
    return render(
        request,
        'posts/post_detail.html',
        {
            'posts': posts,
            'form': CommentForm(),
            'comments': posts.comments.select_related('post'),
        },
    )


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {
                'form': form,
            },
        )
    form.instance.author = request.user
    form.save()
    return redirect(
        'posts:profile',
        form.instance.author,
    )


@login_required
def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    posts = get_object_or_404(Post, pk=pk)
    if posts.author != request.user:
        return redirect(
            'posts:post_detail',
            posts.pk,
        )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=posts,
    )
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {
                'form': form,
                'is_edit': True,
            },
        )
    form.save()
    return redirect(
        'posts:post_detail',
        posts.pk,
    )


@login_required
def add_comment(request: HttpRequest, pk: int) -> HttpResponse:
    posts = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST or None)
    if not form.is_valid():
        return redirect('posts:post_detail', pk=pk)
    form.instance.author = request.user
    form.instance.post = posts
    form.save()
    return redirect(
        'posts:post_detail',
        posts.pk,
    )


@login_required
def follow_index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'posts/follow.html',
        {
            'page_obj': paginate(
                request,
                Post.objects.filter(author__following__user=request.user),
            ),
        },
    )


@login_required
def profile_follow(request: HttpRequest, username: str) -> HttpResponse:
    author = get_object_or_404(User, username=username)
    if (
        request.user != author
        and not Follow.objects.filter(
            user=request.user,
            author=author,
        ).exists()
    ):
        Follow.objects.create(user=request.user, author=author)
    return redirect(
        'posts:profile',
        username,
    )


@login_required
def profile_unfollow(request: HttpRequest, username: str) -> HttpResponse:
    get_object_or_404(
        Follow,
        user=request.user,
        author__username=username,
    ).delete()
    return redirect(
        'posts:profile',
        username,
    )
