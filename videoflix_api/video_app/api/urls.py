# video_app/api/urls.py
from rest_framework import routers
from django.urls import include, path
from .views import DownloadVideoView, VideoViewSet


router = routers.DefaultRouter()

router.register(r'video-list', VideoViewSet, basename='sub-profile')


urlpatterns = [
    path('', include(router.urls)),
    path('<str:video_type>/<str:video_name>/<path:file_path>/', DownloadVideoView.as_view(), name='download-video-file'),
    path('<str:video_type>/<str:video_name>/', DownloadVideoView.as_view(), name='stream_video'),
]

