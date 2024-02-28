import datetime as dt

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from blog.models import Post, Category


COUVIEW = 5


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


def index(request):
    template_name = 'blog/index.html'
    posts = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=dt.datetime.now()
    ).order_by('-pub_date')[:COUVIEW]
    context = {
        'post_list': posts
    }
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=dt.datetime.now()
        ),
        pk=post_id
    )
    context = {
        'post': post,
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ).filter(
            is_published=True,
            slug=category_slug,
        )
    )
    posts = Post.objects.filter(
        is_published=True,
        category__slug=category_slug,
        pub_date__lt=dt.datetime.now()
    )
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, template_name, context)
