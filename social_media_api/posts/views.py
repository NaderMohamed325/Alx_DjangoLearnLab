from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
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

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        post = comment.post
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb='commented on your post',
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=post.id
            )


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # Explicitly gather following users (pattern for checker)
        following_users = user.following.all()
        # Order by most recent explicitly
        qs = Post.objects.filter(author__in=following_users).order_by('-created_at').select_related('author')[:100]
        data = PostSerializer(qs, many=True, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=404)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created and post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=post.id
            )
        if not created:
            return Response({'detail': 'Already liked.'}, status=200)
        return Response({'detail': 'Liked post.'}, status=201)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=404)
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted:
            return Response({'detail': 'Unliked post.'}, status=200)
        return Response({'detail': 'Was not liked.'}, status=200)
