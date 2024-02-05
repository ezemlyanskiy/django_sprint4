from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentCreateForm, PostCreateForm, UserEditForm
from .models import Category, Comment, Post
from .utils import get_base_posts_query

User = get_user_model()


class PostListView(ListView):
    model = Post
    queryset = (
        get_base_posts_query()
        .prefetch_related('comments')
        .filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now()
        )
    )
    template_name = "blog/index.html"
    paginate_by = settings.PAGE_SIZE


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        queryset = get_base_posts_query()
        if self.request.user.id != post.author.id:
            queryset = (
                queryset
                .filter(
                    is_published=True,
                    category__is_published=True,
                    pub_date__lte=timezone.now()
                )
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(
            post__id=self.kwargs.get("pk")
        )
        context["form"] = CommentCreateForm()
        return context


class PostMixin:
    model = Post
    template_name = "blog/create.html"
    form_class = PostCreateForm

    def get_success_url(self):
        return reverse(
            "blog:profile",
            kwargs={"username": self.request.user.username}
        )


class PostDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.user != post.author:
            return redirect("blog:post_detail", post.pk)
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    PostMixin, PostDispatchMixin, LoginRequiredMixin, UpdateView
):
    ...


class PostDeleteView(PostDispatchMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/create.html"
    success_url = reverse_lazy("blog:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostCreateForm(instance=self.object)
        return context


class ProfileDetailView(ListView):
    model = Post
    template_name = "blog/profile.html"
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        username = self.kwargs.get("username")
        return (
            get_base_posts_query()
            .filter(author__username=username)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            "blog:profile", kwargs={"username": self.object.username}
        )


class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/category.html"
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        return (
            get_base_posts_query()
            .prefetch_related('comments')
            .filter(
                category__slug=self.kwargs.get("category_slug"),
                is_published=True,
                pub_date__lte=timezone.now()
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category.objects.values("title", "description"),
            slug=self.kwargs.get("category_slug"),
            is_published=True,
        )
        return context


class CommentMixin:
    model = Comment
    form_class = CommentCreateForm


class CommentDispatchSuccessMixin:
    template_name = "blog/comment.html"

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.author:
            return redirect("blog:post_detail", kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            "blog:post_detail", kwargs={"pk": self.kwargs["post_id"]}
        )


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    template_name = "blog/comments.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(
    CommentMixin, CommentDispatchSuccessMixin, LoginRequiredMixin, UpdateView
):
    ...


class CommentDeleteView(
    LoginRequiredMixin, CommentDispatchSuccessMixin, DeleteView
):
    model = Comment
