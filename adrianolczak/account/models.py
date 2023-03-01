from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"user_photo.{ext}"

    filepath = 'users/{0}/{1}'.format(instance.user.username, filename)

    if default_storage.exists(filepath):
        default_storage.delete(filepath)
    
    return filepath


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, default='users/user_default.png')
    bio = models.CharField(max_length=150, blank=True)
    website_link = models.URLField(max_length=65, blank=True)
    github_link = models.URLField(max_length=65, blank=True)
    twitter_link = models.URLField(max_length=65, blank=True)
    instagram_link = models.URLField(max_length=65, blank=True)
    facebook_link = models.URLField(max_length=65, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
