from django import forms
from .models import NewsComent


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComent
        fields = ['content']