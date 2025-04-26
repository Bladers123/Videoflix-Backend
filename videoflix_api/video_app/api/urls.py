# video_app/api/urls.py
from rest_framework import routers
from django.urls import include, path, re_path
from .views import DownloadVideoView, VideoViewSet, serve_ftp_image


router = routers.DefaultRouter()

router.register(r'video-list', VideoViewSet, basename='video-list')


urlpatterns = [
    path('', include(router.urls)),
    path('<str:video_type>/<str:video_name>/<path:file_path>/', DownloadVideoView.as_view(), name='download-video-file'),
    path('<str:video_type>/<str:video_name>/', DownloadVideoView.as_view(), name='stream_video'),
    re_path(r"^ftp-images/(?P<image_path>.+)$", serve_ftp_image, name="video-ftp-images"),
]

