from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import logging

from .models import User, Task


logger = logging.getLogger(__name__)


class UserCreateSerializer(BaseUserCreateSerializer):
    username = serializers.CharField(read_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']

    def save(self, **kwargs):
        self.validated_data['password'] = make_password(
            self.validated_data['password'])
        self.validated_data['username'] = self.validated_data['email'].split(
            '@')[0]
        self.instance = User.objects.create(**self.validated_data)
        self.instance.save()
        return self.instance


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username']


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']



class TaskCreateSerializer(serializers.ModelSerializer):
    # is_done = serializers.BooleanField(read_only=True)
    class Meta:
        model = Task
        fields = ['name', 'description', 'is_done']
    
    
    def create(self, validated_data):
        user = self.context['request'].user
        task = Task.objects.create(user=user, **validated_data)
        return task


class TaskSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'is_done', 'user', 'created_at']
