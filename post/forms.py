from django import forms
from .models import PostComment, Post, PostReply


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']


class PostReplyForm(forms.ModelForm):
    class Meta:
        model = PostReply
        fields = ['reply_type', 'comment', 'text']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content']
