from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
from django.http import HttpRequest

# Create your views here.

def book_list(request):
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