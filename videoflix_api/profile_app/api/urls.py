# profile_app/api/urls.py
from rest_framework import routers
from django.urls import include, path
from .views import ProfileViewSet, SubProfileViewSet, serve_ftp_image


router = routers.DefaultRouter()

router.register(r'profile-list', ProfileViewSet, basename='profile')
router.register(r'sub-profile-list', SubProfileViewSet, basename='sub-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('ftp-images/<path:image_path>/', serve_ftp_image, name='serve_ftp_image'),
]