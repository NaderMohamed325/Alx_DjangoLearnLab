from django.urls import path, include
from .views import  BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'book_all', BookViewSet, basename='book_all')

urlpatterns = [
    path("", include(router.urls)),  
     path('auth/', include('rest_authtoken.urls')),
]
