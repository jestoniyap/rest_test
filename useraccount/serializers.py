from django.contrib.auth.models import User

from rest_framework import serializers

from useraccount.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'username', 'email', 'groups')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('pk', 'created_on', 'picture', 'user')