

from .views import (
      # Import your views here
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:id>/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:id>/', BookDeleteView.as_view(), name='book-delete'),
]