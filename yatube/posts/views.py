from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import paginate
from posts.forms import CommentForm, PostForm
from posts.models import Group, Post, User


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related('author')
    page = paginate(request, posts)
    return render(
        request,
        'posts/index.html',
        {
            'page_obj': page,
        },
    )


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author', 'group')
    page = paginate(request, posts)
    return render(
        request,
        'posts/group_list.html',
        {
            'page_obj': page,
            'group': group,
        },
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    users = get_object_or_404(User, username=username)
    posts = users.posts.select_related('author')
    page = paginate(request, posts)
    return render(
        request,
        'posts/profile.html',
        {
            'page_obj': page,
            'users': users,
        },
    )


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    posts = get_object_or_404(Post, pk=pk)
    comments = posts.comments.all()
    return render(
        request,
        'posts/post_detail.html',
        {
            'posts': posts,
            'form': CommentForm(),
            'comments': comments,
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