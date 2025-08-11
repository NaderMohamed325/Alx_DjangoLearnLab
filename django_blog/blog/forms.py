# blog/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """Extended user registration form with email field."""
    email = forms.EmailField()  # Add email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Fields in the form
