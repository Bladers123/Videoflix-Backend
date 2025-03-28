# profile_app/api/urls.py
from rest_framework import routers
from django.urls import include, path
from .views import ProfilePictureDownloadView, ProfilePictureUploadView, ProfileViewSet, SubProfileViewSet


router = routers.DefaultRouter()


router.register(r'profile-list', ProfileViewSet, basename='profile')
router.register(r'sub-profile-list', SubProfileViewSet, basename='sub-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', ProfilePictureUploadView.as_view(), name='profile_picture_upload'),
    path('download/<str:filename>/', ProfilePictureDownloadView.as_view(), name='profile_picture_download'),

]