from django import forms
from .models import NewsComment, Reply


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ['content']


class NewsReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_type', 'comment', 'text']