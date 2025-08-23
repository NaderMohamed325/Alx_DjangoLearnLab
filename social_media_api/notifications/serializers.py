from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'read', 'created_at']
