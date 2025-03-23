# video_app/api/urls.py
from django.urls import path
from .views import StreamVideoView, VideoTestView

urlpatterns = [
    path('', VideoTestView.as_view(), name='video-test'),
    path('<str:video_name>/', StreamVideoView.as_view(), name='stream_video'),
]
