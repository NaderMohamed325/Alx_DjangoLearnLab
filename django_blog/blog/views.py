# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import UserRegisterForm

def register_view(request):
    """Handle user registration."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile_view(request):
    """Display user profile."""
    return render(request, 'blog/profile.html')

@login_required
def home_view(request):
    """Display home page."""
    post_list = Post.objects.all()  # Assuming you have a Post model
    return render(request, 'blog/home.html', {"posts": post_list})
