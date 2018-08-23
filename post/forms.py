from django import forms
from .models import PostComent


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComent
        fields = ['content']