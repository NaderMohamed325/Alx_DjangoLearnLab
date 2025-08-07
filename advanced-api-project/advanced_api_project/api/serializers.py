from rest_framework import serializers
from datetime import datetime
from .models import Book, Author

# -------------------------------
# Serializer for the Book model
# -------------------------------
# This serializer converts Book model instances to JSON format and vice versa.
# It includes all model fields and implements a custom validation rule
# to ensure that the publication year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Includes all fields from the Book model

    # Custom field-level validation for the 'publication_year' field
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# ----------------------------------
# Serializer for the Author model
# ----------------------------------
# This serializer is responsible for serializing the Author model.
# It includes the 'name' field and a nested list of related Book objects.
# The nested 'books' field uses BookSerializer to represent each book.
# 
# Relationship Handling:
# - The Book model has a ForeignKey to Author with related_name='books'.
# - This allows the AuthorSerializer to access all related books using author.books.all().
# - The 'books' field is marked read_only to allow read-only nested serialization.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested list of books written by the author

    class Meta:
        model = Author
        fields = ['name', 'books']  # Only include name and the related books
