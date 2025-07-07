# delete.md

# Delete the book you created and confirm the deletion by retrieving all books

from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

print(Book.objects.all())

# Expected Output:

# QuerySet should be empty after deletion.

# Example: <QuerySet []>
