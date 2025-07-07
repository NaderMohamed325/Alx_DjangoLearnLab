# retrieve.md

# Retrieve and display all attributes of the book you just created
from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(f"ID: {book.id}\nTitle: {book.title}\nAuthor: {book.author}\nPublication Year: {book.publication_year}")

# Expected Output:
# ID: 1
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
