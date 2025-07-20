from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Library, Book
from django.http import HttpRequest

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The library object is automatically available as 'library' in the template
        # The books can be accessed via library.books.all in the template
        return context

# Authentication Views
def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('book_list')  # Redirect to book list after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

class CustomLoginView(LoginView):
    """Custom login view using Django's built-in LoginView"""
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/books/'  # Redirect to book list after login

class CustomLogoutView(LogoutView):
    """Custom logout view using Django's built-in LogoutView"""
    template_name = 'relationship_app/logout.html'