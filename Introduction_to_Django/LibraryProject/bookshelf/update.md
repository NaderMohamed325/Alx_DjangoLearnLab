# update.md

# Update the title of "1984" to "Nineteen Eighty-Four" and save the changes
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Expected Output:
# Title successfully updated.
# Example: book.title returns "Nineteen Eighty-Four"
