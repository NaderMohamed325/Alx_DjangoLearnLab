# blog/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class UserRegisterForm(UserCreationForm):
    """Extended user registration form with email field."""
    email = forms.EmailField()  # Add email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Fields in the form

class PostForm(forms.ModelForm):
    """Form for creating and updating blog posts."""
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post here...', 'rows': 6}),
        }
