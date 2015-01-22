from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.authentication import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import UserSerializer, UserProfileSerializer

from useraccount.models import UserProfile


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

