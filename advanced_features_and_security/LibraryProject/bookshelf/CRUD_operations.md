# CRUD_operations.md

# Django Shell Commands and Outputs for Full CRUD Cycle

# 1. CREATE

from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)

# Output:

# <Book: 1984 by George Orwell (1949)>

# 2. RETRIEVE

book = Book.objects.get(title="1984")
print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")

# Output:

# ID: 1, Title: 1984, Author: George Orwell, Year: 1949

# 3. UPDATE

book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)

# Output:

# Nineteen Eighty-Four

# 4. DELETE

book.delete()
print(Book.objects.all())

# Output:

# <QuerySet []>
