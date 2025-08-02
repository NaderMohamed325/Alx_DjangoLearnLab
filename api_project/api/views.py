from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer  

class BookListCreateAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer