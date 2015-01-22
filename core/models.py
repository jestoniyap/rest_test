from django.contrib.auth.models import User
from django.db import models

from useraccount.models import UserProfile


class Post(models.Model):
    """
    Post Model with integration of Auth.User class
    """

    message = models.CharField('Mesage', max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True, auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(UserProfile, null=True, blank=True, related_name='post_author')
    user_who_liked = models.ManyToManyField(UserProfile, blank=True, null=True, related_name='user_who_liked')

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __unicode__(self):
        if self.author.user.last_name and self.author.user.first_name:
            return "%s %s" % (self.author.user.first_name, self.author.user.last_name)
        return self.author.user.username

    def likes(self):
        return self.user_who_liked.all().count()

    def comments(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    """
    Comment Model with integration of Auth.User class
    """

    message = models.CharField('Mesage', max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True, auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(UserProfile, null=True, blank=True, related_name='comment_author')
    post = models.ForeignKey(Post, null=True, blank=True, related_name='comment_post')

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __unicode__(self):
        if self.author.user.last_name and self.author.user.first_name:
            return "%s %s" % (self.author.user.first_name, self.author.user.last_name)
        return self.author.user.username
