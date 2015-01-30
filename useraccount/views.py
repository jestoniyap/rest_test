import os

from base64 import b64decode

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from rest_framework import viewsets
from rest_framework.authentication import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import UserSerializer, UserProfileSerializer

from useraccount.models import UserProfile, profile_image_path




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileView(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(userprofile)

            return Response(serializer.data)
        except Exception, e:
            print e

userprofile_view = UserProfileView.as_view()


class UploadProfilePictureView(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            filepath = profile_image_path(userprofile, 'path.png')
            image_data = b64decode(request.DATA['file'])

            userprofile.picture = ContentFile(image_data, filepath)
            userprofile.save()

            serializer = UserProfileSerializer(userprofile)

            return Response(serializer.data)
        except Exception, e:
            print e

upload_profile_picture_view = UploadProfilePictureView.as_view()

