from rest_framework import routers
from django.urls import include, path
from .views import ProfileViewSet, SubProfileViewSet


router = routers.DefaultRouter()




router.register(r'profile-list', ProfileViewSet, basename='profile')
router.register(r'sub-profile-list', SubProfileViewSet, basename='sub-profile')

urlpatterns = [
    path('', include(router.urls)),
]