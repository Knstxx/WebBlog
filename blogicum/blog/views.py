import datetime as dt

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404

from blog.models import Post, Category, User, Comment
from .forms import PostForm, CommentForm, UserUpdateForm


PAGIN_COUNT = 10


class IndexListView(ListView):

    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=dt.datetime.now()
    ).annotate(comment_count=Count('comments'))
    ordering = '-pub_date'
    paginate_by = PAGIN_COUNT


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        current_user = self.request.user
        is_owner = current_user == post.author
        if (not is_owner and not post.is_published):
            raise Http404("Страница не найдена")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.object)
        return context


class ProfileListView(ListView):

    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PAGIN_COUNT

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        current_user = self.request.user
        is_owner = current_user == user
        if is_owner:
            return user.posts.all().annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        else:
            return user.posts.all().filter(
                is_published=True,
                pub_date__lt=dt.datetime.now()
            ).annotate(comment_count=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        context['profile'] = user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={
            'username': self.request.user
        })


class CategoryListView(ListView):
    model = Post
    paginate_by = PAGIN_COUNT
    template_name = 'blog/category.html'

    def get_queryset(self):
        return Post.objects.filter(
            is_published=True,
            category__slug=self.kwargs['category_slug'],
            pub_date__lt=dt.datetime.now()
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')

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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={
            'username': self.request.user
        })


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        if post.author != request.user:
            return redirect('blog:post_detail', post_id=post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = {'instance': context['object']}
        return context

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        if post.author != request.user:
            return redirect('blog:post_detail', post_id=post.id)
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.kwargs.get('post_id')
        })


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_id'))
        if comment.author != request.user:
            return redirect('blog:post_detail', post_id=comment.post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.object.post.id
        })


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = {'instance': context['object']}
        return context

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_id'))
        if comment.author != request.user:
            return redirect('blog:post_detail', post_id=comment.post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.object.post.id
        })
