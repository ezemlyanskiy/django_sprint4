from django.shortcuts import redirect
from django.urls import reverse

from .forms import CommentCreateForm, PostCreateForm
from .models import Comment, Post


class PostMixin:
    model = Post
    template_name = 'blog/create.html'
    form_class = PostCreateForm

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.user != post.author:
            return redirect('blog:post_detail', post.pk)
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Comment
    form_class = CommentCreateForm


class CommentDispatchSuccessMixin:
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.author:
            return redirect('blog:post_detail', kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )
