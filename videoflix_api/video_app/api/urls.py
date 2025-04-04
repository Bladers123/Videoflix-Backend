# video_app/api/urls.py
from django.urls import path
from .views import DownloadVideoView, VideoTestView

urlpatterns = [
    path('', VideoTestView.as_view(), name='video-test'),
    path('<str:video_name>/<str:file_name>/', DownloadVideoView.as_view()),
    path('<str:video_name>/', DownloadVideoView.as_view(), name='stream_video'),
]