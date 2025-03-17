# profile_app
from django.db import models
from authentication_app.models import CustomUser



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=100, blank=True, default='')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=150, blank=True, default='')
    phone = models.CharField(max_length=25, blank=True, default='')
    email = models.EmailField(blank=True, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"





class SubProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="subprofile")
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='profile_images', null=True, blank=True)

    def __str__(self):
        return self.name
