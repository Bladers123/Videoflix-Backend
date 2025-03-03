from django.urls import path
from .views import AuthTestView

urlpatterns = [
    path('', AuthTestView.as_view(), name='auth-test'),
]
