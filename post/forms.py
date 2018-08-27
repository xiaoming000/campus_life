from django import forms
from .models import PostComent, Post


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComent
        fields = ['content']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content']
