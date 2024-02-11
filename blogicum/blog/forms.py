from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Post

User = get_user_model()


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'is_published')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format=('d E Y, H:i'), attrs={'type': 'datetime-local'}
            ),
        }


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
