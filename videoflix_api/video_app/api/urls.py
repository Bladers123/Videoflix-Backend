# video_app/api/urls.py
from django.urls import path
from .views import DownloadVideoView, VideoNameView



urlpatterns = [
    path('videoname/', VideoNameView.as_view(), name='videoname'),
    path('<str:video_type>/<str:video_name>/<path:file_path>/', DownloadVideoView.as_view(), name='download-video-file'),
    path('<str:video_type>/<str:video_name>/', DownloadVideoView.as_view(), name='stream_video'),
]
