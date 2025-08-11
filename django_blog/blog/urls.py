# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home_view,
    register_view,
    profile_view,
    logout_view,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    comment_create,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
)

urlpatterns = [
    # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    
    # Home URLs
    path('home/', home_view, name='home'),
    path('', home_view, name='index'),
    
    # Post CRUD URLs
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # Comment CRUD URLs
    path('posts/<int:pk>/comment/', comment_create, name='comment_create'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment_create_class'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
