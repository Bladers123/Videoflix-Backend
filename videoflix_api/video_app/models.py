# video_app/models.py
from django.db import models
from django.conf import settings

class Video(models.Model):
    VIDEO_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('clip', 'Clip'),
    ]

    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    video_type = models.CharField(
        max_length=10,
        choices=VIDEO_TYPE_CHOICES,
        default='movie',
        help_text="Bitte auswählen: movie oder clip"
    )

    def __str__(self):
        return self.title
