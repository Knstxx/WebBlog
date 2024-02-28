import datetime as dt
import pytz
# нашёл библиотеку часовых поясов.
# Есть возможность настраивать работу сайта, в зависимости от региона

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from blog.models import Post, Category
from .forms import PostForm, CommentForm

TZ = pytz.timezone('UTC')

@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class IndexListView(ListView):

    model = Post
    queryset = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=dt.datetime.now(TZ)
    )
    ordering = '-pub_date'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post

    def get_object(self):
        post_id = self.kwargs.get("post_id")
        return get_object_or_404(Post, id=post_id)


class ProfileListView(ListView):

    model = Post
    queryset = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=dt.datetime.now(TZ)
    )
    ordering = '-pub_date'
    paginate_by = 10


class CategoryListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            is_published=True,
            category__slug=self.kwargs['category_slug'],
            pub_date__lt=dt.datetime.now(TZ)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.values(
                'title', 'description'
            ).filter(
                is_published=True,
                slug=self.kwargs['category_slug'],
            )
        )
        return context






'''
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
'''