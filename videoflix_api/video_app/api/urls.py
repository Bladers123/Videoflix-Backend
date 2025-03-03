from django.urls import path
from .views import VideoTestView

urlpatterns = [
    path('', VideoTestView.as_view(), name='video-test'),
]
