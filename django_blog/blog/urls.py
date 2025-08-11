# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, register_view, profile_view


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('home/', home_view, name='home')
]
