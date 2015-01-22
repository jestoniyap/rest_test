from django.contrib import admin

from core.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
