import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author():
    """Query all books by a specific author."""
    print("=== Books by Author Queries ===")
    
    # Method 1: Using the related_name 'books'
    try:
        author_name = "J.K. Rowling"  # Example author name
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using the related_name from ForeignKey
        
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
    
    # Method 2: Using filter on Book model
    try:
        author_name = "George Orwell"  # Example author name
        books = Book.objects.filter(author__name=author_name)
        
        print(f"\nBooks by {author_name} (using filter):")
        for book in books:
            print(f"  - {book.title}")
    except Exception as e:
        print(f"Error: {e}")

def query_books_in_library():
    """List all books in a library."""
    print("\n=== Books in Library Queries ===")
    
    try:
        library_name = "Central Library"  # Example library name
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Using the ManyToManyField
        
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
    
    # Alternative method using prefetch_related for better performance
    try:
        library = Library.objects.prefetch_related('books__author').get(name=library_name)
        print(f"\nBooks in {library.name} (optimized query):")
        for book in library.books.all():
            print(f"  - {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

def query_librarian_for_library():
    """Retrieve the librarian for a library."""
    print("\n=== Librarian for Library Queries ===")
    
    # Method 1: Using the related_name 'librarian'
    try:
        library_name = "Central Library"  # Example library name
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Using the related_name from OneToOneField
        
        print(f"Librarian for {library_name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'.")
    
    # Method 2: Using Librarian model
    try:
        library_name = "Central Library"
        librarian = Librarian.objects.get(library__name=library_name)
        
        print(f"Librarian for {library_name} (using Librarian model): {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian found for library '{library_name}'.")

def create_sample_data():
    """Create sample data for testing queries."""
    print("=== Creating Sample Data ===")
    
    # Create authors
    author1, created = Author.objects.get_or_create(name="J.K. Rowling")
    author2, created = Author.objects.get_or_create(name="George Orwell")
    
    # Create books
    book1, created = Book.objects.get_or_create(
        title="Harry Potter and the Philosopher's Stone",
        defaults={'author': author1}
    )
    book2, created = Book.objects.get_or_create(
        title="Harry Potter and the Chamber of Secrets",
        defaults={'author': author1}
    )
    book3, created = Book.objects.get_or_create(
        title="1984",
        defaults={'author': author2}
    )
    book4, created = Book.objects.get_or_create(
        title="Animal Farm",
        defaults={'author': author2}
    )
    
    # Create library
    library, created = Library.objects.get_or_create(name="Central Library")
    
    # Add books to library
    library.books.add(book1, book2, book3, book4)
    
    # Create librarian
    librarian, created = Librarian.objects.get_or_create(
        name="Alice Johnson",
        defaults={'library': library}
    )
    
    print("Sample data created successfully!")

if __name__ == "__main__":
    # Create sample data first
    create_sample_data()
    
    # Run the queries
    query_books_by_author()
    query_books_in_library()
    query_librarian_for_library()
    
    print("\n=== Query Examples Complete ===")