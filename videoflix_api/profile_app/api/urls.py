from django.urls import path
from .views import ProfileTestView

urlpatterns = [
    path('', ProfileTestView.as_view(), name='profile-test'),
]
