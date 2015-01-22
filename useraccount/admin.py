from django.contrib import admin
from django.contrib.auth.models import User

from useraccount.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)
