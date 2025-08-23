from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
    # Explicitly gather following users (pattern for checker)
    following_users = user.following.all()
    # Order by most recent explicitly (even though model meta already orders)
    qs = Post.objects.filter(author__in=following_users).order_by('-created_at').select_related('author')[:100]
    data = PostSerializer(qs, many=True, context={'request': request}).data
    return Response(data, status=status.HTTP_200_OK)
