from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserSerializer(serializers.ModelSerializer):
	followers_count = serializers.SerializerMethodField(read_only=True)
	following_count = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = User
		fields = [
			'id', 'username', 'email', 'first_name', 'last_name', 'bio',
			'profile_picture', 'followers_count', 'following_count'
		]
		read_only_fields = ['id', 'followers_count', 'following_count']

	def get_followers_count(self, obj):
		return obj.followers.count()

	def get_following_count(self, obj):
		return obj.following.count()


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({'password': 'Password fields did not match.'})
		return attrs

	def create(self, validated_data):
		validated_data.pop('password2')
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		Token.objects.get_or_create(user=user)
		return user


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(read_only=True)

	def validate(self, attrs):
		user = authenticate(username=attrs['username'], password=attrs['password'])
		if not user:
			raise serializers.ValidationError('Invalid credentials')
		attrs['user'] = user
		token, _ = Token.objects.get_or_create(user=user)
		attrs['token'] = token.key
		return attrs


class ProfileUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'bio', 'profile_picture']
