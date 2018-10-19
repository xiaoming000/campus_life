from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile
from django import forms


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class EditProForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'introduce']