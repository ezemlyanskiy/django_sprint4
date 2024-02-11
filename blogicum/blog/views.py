from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentCreateForm, PostCreateForm
from .mixins import (
    CommentDispatchSuccessMixin, CommentMixin, PostDispatchMixin, PostMixin
)
from .models import Category, Comment, Post
from .utils import get_base_posts_query

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = settings.PAGE_SIZE
    queryset = (
        get_base_posts_query()
        .filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now(),
        )
    )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        queryset = get_base_posts_query()
        if self.request.user.id != post.author.id:
            queryset = (
                queryset
                .filter(
                    category__is_published=True,
                    is_published=True,
                    pub_date__lte=timezone.now(),
                )
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (
            Comment.objects
            .prefetch_related('author')
            .filter(post__id=self.kwargs['pk'])
            .defer('post')
        )
        context['form'] = CommentCreateForm()
        return context


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    PostMixin, PostDispatchMixin, LoginRequiredMixin, UpdateView
):
    ...


class PostDeleteView(
    PostMixin, PostDispatchMixin, LoginRequiredMixin, DeleteView
):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCreateForm(instance=self.object)
        return context


class ProfileDetailView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        return (
            get_base_posts_query()
            .filter(author__username=self.kwargs['username'])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User.objects.only(
                'username',
                'first_name',
                'last_name',
                'date_joined',
                'is_staff',
            ),
            username=self.kwargs['username']
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = (
        'first_name',
        'last_name',
        'username',
        'email',
    )
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.object.username}
        )


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        return (
            get_base_posts_query()
            .filter(
                category__slug=self.kwargs.get('category_slug'),
                is_published=True,
                pub_date__lte=timezone.now(),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.values(
                'title',
                'description',
            ),
            slug=self.kwargs['category_slug'],
            is_published=True,
        )
        return context


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    template_name = 'blog/comments.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )


class CommentUpdateView(
    CommentMixin, CommentDispatchSuccessMixin, LoginRequiredMixin, UpdateView
):
    ...


class CommentDeleteView(
    CommentMixin, CommentDispatchSuccessMixin, LoginRequiredMixin, DeleteView
):
    ...
