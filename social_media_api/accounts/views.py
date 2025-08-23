from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ProfileUpdateSerializer,
)

CustomUser = get_user_model()


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            data = UserSerializer(user).data
            data['token'] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = serializer.validated_data['token']
            data = UserSerializer(user).data
            data['token'] = token
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, user_id):  # follow user
        if request.user.id == user_id:
            return Response({'detail': 'Cannot follow yourself.'}, status=400)
        try:
            target = self.get_queryset().get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)
        request.user.following.add(target)
        return Response({'detail': f'Now following {target.username}.'}, status=200)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, user_id):  # unfollow user
        if request.user.id == user_id:
            return Response({'detail': 'Cannot unfollow yourself.'}, status=400)
        try:
            target = self.get_queryset().get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)
        request.user.following.remove(target)
        return Response({'detail': f'Stopped following {target.username}.'}, status=200)

    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)