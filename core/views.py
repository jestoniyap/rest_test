from rest_framework import viewsets
from rest_framework.authentication import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import PostSerializer, CommentSerializer

from core.models import Post, Comment
from useraccount.models import UserProfile


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostView(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        try:
            userprofile = UserProfile.objects.get(user=request.user)

            posts = Post.objects.filter(author=userprofile)

            serializer = PostSerializer(posts, many=True)

            return Response(serializer.data)

        except Exception, e:
            print e

    def post(self, request):

        try:
            message = request.DATA.get('message')

            userprofile = UserProfile.objects.get(user=request.user)
            post = Post.objects.create(message=message, author=userprofile)

            content = {
                'message': 'Created Successful',
            }
            return Response(content)

        except Exception, e:
            print e

post_view = PostView.as_view()


class LikeView(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            post_id = request.DATA.get('post_id')
            userprofile = UserProfile.objects.get(user=request.user)
            is_liked = False

            try:
                post = Post.objects.get(pk=post_id)
            except Exception, e:
                print e
                post = None

            if post:
                if userprofile in post.user_who_liked.all():
                    post.user_who_liked.remove(userprofile)
                else:
                    post.user_who_liked.add(userprofile)
                    is_liked = True

            content = {
                'message': 'Toggled Successful',
                'is_liked': is_liked,
                'likes': post.likes()
            }
            return Response(content)

        except Exception, e:
            print e

like_view = LikeView.as_view()


class CommentView(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        try:
            try:
                post = Post.objects.get(pk=post_id)
            except Exception, e:
                print e
                post = None

            if post:
                comments = Comment.objects.filter(post=post)

                serializer = CommentSerializer(comments, many=True)

                return Response(serializer.data)

        except Exception, e:
            print e


    def post(self, request, post_id):
        try:
            message = request.DATA.get('message')
            userprofile = UserProfile.objects.get(user=request.user)

            try:
                post = Post.objects.get(pk=post_id)
            except Exception, e:
                print e
                post = None

            if post:
                comment = Comment.objects.create(message=message, author=userprofile, post=post)
                

            content = {
                'message': 'Created Successful'
            }
            return Response(content)

        except Exception, e:
            print e

comment_view = CommentView.as_view()