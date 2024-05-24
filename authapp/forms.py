from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    api_key = forms.CharField(max_length=40, required=False)  # New field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'api_key']
