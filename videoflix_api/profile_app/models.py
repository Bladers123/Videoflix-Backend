from django.db import models
from authentication_app.models import CustomUser


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="profiles")
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='profile_images', null=True, blank=True)

    def __str__(self):
        return self.name
