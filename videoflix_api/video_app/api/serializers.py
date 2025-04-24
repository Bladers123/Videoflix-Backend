# video_app/serializers.py
import os
from django.urls import reverse
from rest_framework import serializers
from ..models import Video

            

class VideoSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description',
            'file_size', 'uploaded_at',
            'video_type', 'video_file',
            'thumbnail',
        ]

    def get_thumbnail(self, obj):
        if not obj.thumbnail:
            return None

        basename = os.path.splitext(os.path.basename(obj.thumbnail.name))[0]
        filename = os.path.basename(obj.thumbnail.name)
        image_path = f"{obj.video_type}s/{basename}/{filename}"
        url = reverse('video-ftp-images', kwargs={'image_path': image_path})
        return self.context['request'].build_absolute_uri(url)
