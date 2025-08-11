# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import UserRegisterForm, PostForm, CommentForm


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect("profile")  # redirect logged-in users

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

def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')

@login_required
def home_view(request):
    """Display home page."""
    post_list = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': post_list})

# Class-based views for Post CRUD operations

class PostListView(ListView):
    """View to display all blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class PostDetailView(DetailView):
    """View to display a single blog post."""
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        """Add comment form to context."""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """View to create a new blog post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        """Set the author to the current logged-in user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update an existing blog post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        """Set the author to the current logged-in user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a blog post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
        
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted!')
        return super().delete(request, *args, **kwargs)

# Comment views
@login_required
def comment_create(request, pk):
    """Create a new comment on a post."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return redirect('post_detail', pk=post.pk)

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Class-based view to create a new comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Set post and author before saving."""
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been added!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return to the post detail page after creating the comment."""
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update an existing comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def get_success_url(self):
        """Return to the post detail page after updating the comment."""
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
    
    def form_valid(self, form):
        """Show success message and update the comment."""
        messages.success(self.request, 'Your comment has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def get_success_url(self):
        """Return to the post detail page after deleting the comment."""
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
    
    def delete(self, request, *args, **kwargs):
        """Show success message and delete the comment."""
        messages.success(self.request, 'Your comment has been deleted!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
