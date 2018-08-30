from django import forms
from .models import PostComent, Post, PostReply


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComent
        fields = ['content']


class PostReplyForm(forms.ModelForm):
    class Meta:
        model = PostReply
        fields = ['reply_type', 'post_comment', 'content']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content']
