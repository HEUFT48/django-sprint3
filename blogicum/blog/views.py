from django.http import Http404
from django.shortcuts import render
from .models import Post, Category
from django.utils import timezone
from django.db.models import Q


def index(request):
    posts = Post.objects.select_related('category', 'location', 'author').filter(
        Q(is_published=True),
        Q(category__is_published=True),
        Q(pub_date__lte=timezone.now())
    ).order_by('-pub_date')[:5]

    context = {
        'post_list': posts,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = Post.objects.select_related('category', 'location', 'author').filter(
        Q(id=id),
        Q(is_published=True),
        Q(category__is_published=True),
        Q(pub_date__lte=timezone.now())
    ).first()

    if not post:
        raise Http404("Публикация не найдена")

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = Category.objects.filter(
        slug=category_slug,
        is_published=True
    ).first()

    if not category:
        raise Http404("Категория не найдена")

    posts = Post.objects.select_related('category', 'location', 'author').filter(
        Q(category=category),
        Q(is_published=True),
        Q(pub_date__lte=timezone.now())
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, 'blog/category.html', context)
