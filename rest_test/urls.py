from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from core.models import Post
from core import views as core_views
from useraccount import views as useraccount_views
from useraccount.models import UserProfile


router = routers.DefaultRouter()
router.register(r'users', useraccount_views.UserViewSet)
router.register(r'user-profiles', useraccount_views.UserProfileViewSet)
router.register(r'posts', core_views.PostViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rest_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   	url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    
    # APIViews
    url(r'^api/posts/', 'core.views.post_view', name='post_view'),
    url(r'^api/toggle-like/', 'core.views.like_view', name='like_view'),
    url(r'^api/comments/(?P<post_id>\d+)/$', 'core.views.comment_view', name='comment_view'),
    url(r'^api/userprofile/', 'useraccount.views.userprofile_view', name='userprofile_view'),
    url(r'^api/upload-profile-picture/', 'useraccount.views.upload_profile_picture_view', name='upload_profile_picture_view')

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
