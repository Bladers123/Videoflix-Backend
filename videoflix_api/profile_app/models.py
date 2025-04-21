# profile_app/models.py
from django.db import models
from authentication_app.models import CustomUser
from video_app.models import Video



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=100, blank=True, default='')
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=150, blank=True, default='')
    phone = models.CharField(max_length=25, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    img = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SubProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="subprofile")
    name = models.CharField(max_length=100)
    favouriteVideos = models.ManyToManyField(Video, related_name='subprofile_favorites', blank=True)

    def __str__(self):
        return self.name


