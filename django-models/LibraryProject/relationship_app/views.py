from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib import messages
from .models import Library, Book, UserProfile, Author
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

# Role checking functions
def is_admin(user):
    """Check if user has Admin role"""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Check if user has Librarian role"""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Check if user has Member role"""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    """Admin-only view"""
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian-only view"""
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    """Member-only view"""
    return render(request, 'relationship_app/member_view.html')

# Permission-secured views for book operations
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book - requires can_add_book permission"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            try:
                author = Author.objects.get(id=author_id)
                book = Book.objects.create(title=title, author=author)
                messages.success(request, f'Book "{book.title}" has been added successfully!')
                return redirect('book_list')
            except Author.DoesNotExist:
                messages.error(request, 'Selected author does not exist.')
        else:
            messages.error(request, 'Please provide both title and author.')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """View to edit an existing book - requires can_change_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            try:
                author = Author.objects.get(id=author_id)
                book.title = title
                book.author = author
                book.save()
                messages.success(request, f'Book "{book.title}" has been updated successfully!')
                return redirect('book_list')
            except Author.DoesNotExist:
                messages.error(request, 'Selected author does not exist.')
        else:
            messages.error(request, 'Please provide both title and author.')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """View to delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" has been deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})