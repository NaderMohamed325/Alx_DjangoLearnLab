from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class BookListView(generics.ListAPIView):
    """
    Retrieve a list of all books.
    Supports filtering by title, author name, and publication year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 🔍 Filterable query parameters
    filterset_fields = ['title', 'author', 'publication_year']

    # 🔎 Search query (fuzzy)
    search_fields = ['title', 'author__name']

    # ⬇️ Sort by any of these fields
    ordering_fields = ['title', 'publication_year']

# -----------------------------
# 🔍 Retrieve a single book by ID
# -----------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]


# -----------------------------
# ➕ Create a new book
# -----------------------------
class BookCreateView(generics.CreateAPIView):
    """
    Create a new book. Validates data before saving.
    Only authenticated users can add new books.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# 🔄 Update an existing book
# -----------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    Update a book using PATCH.
    Only authenticated users can update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            book = self.get_object()
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            updated_book = serializer.save()
            return Response(BookSerializer(updated_book).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# ❌ Delete a book
# -----------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book by ID.
    Only staff users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        try:
            book = self.get_object()
            book.delete()
            return Response({"detail": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
