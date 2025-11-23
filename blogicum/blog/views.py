from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .constants import POSTS_PER_PAGE_INDEX
from .models import Category, Post


def index(request):
    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:POSTS_PER_PAGE_INDEX]

    context = {
        'post_list': posts,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        id=id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, 'blog/category.html', context)
