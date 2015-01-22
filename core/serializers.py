from django.contrib.auth.models import User

from rest_framework import serializers
from useraccount.serializers import UserProfileSerializer

from core.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()

    class Meta:
        model = Post
        fields = ('pk', 'message', 'created_on', 'author', 'likes', 'comments')


class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = ('pk', 'message', 'created_on', 'author', 'post')