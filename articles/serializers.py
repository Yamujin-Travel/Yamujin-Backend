
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'nickname', 'profile_img')


class BaseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

class PostListSerializer(BaseSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'user')

class PostSerializer(BaseSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)
