# relationship_app/query_samples.py

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def query_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)  # ✅ required filter
        print(f"Books by {author.name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name: {author_name}")

# List all books in a library
def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # This is allowed with ManyToManyField
        print(f"Books in {library.name} Library:")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"No library found with name: {library_name}")

# Retrieve the librarian for a library
def get_librarian_of_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # ✅ One-to-One query
        print(f"Librarian of {library.name} Library: {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library found with name: {library_name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name} Library")

if __name__ == '__main__':
    query_books_by_author("Nader Mohamed")
    print()
    list_books_in_library("Downtown Public Library")
    print()
    get_librarian_of_library("Downtown Public Library")
