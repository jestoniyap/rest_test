import os
import uuid

from django.contrib.auth.models import User
from django.db import models

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps
    

def profile_image_path(instance=None, filename=None, user=None):
    """ This is where the path for the profile image will go """
    folder = 'profile'
    user = instance.user
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" %(uuid.uuid4(), ext)
    return os.path.join(folder, user.username, new_filename)

class UserProfile(models.Model):
    """
    UserProfile Model with integration of Auth.User class
    """

    created_on = models.DateTimeField(auto_now=True, auto_now_add=True)
    picture = models.ImageField(null=True, blank=True, upload_to=profile_image_path)
    user = models.OneToOneField(User)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args,**kwargs)
        filename = str(self.picture.path)
        image = Image.open(filename)

        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")

        image_resize = image.resize((200,200), Image.ANTIALIAS)
        image_resize.save(filename, 'PNG', quality=75)

    def __unicode__(self):
        if self.user.last_name and self.user.first_name:
            return "%s %s" % (self.user.first_name, self.user.last_name)
        return self.user.username
