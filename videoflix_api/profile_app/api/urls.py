from rest_framework import routers
from django.urls import include, path
from .views import ProfileViewSet


router = routers.DefaultRouter()




router.register(r'profile-list', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]