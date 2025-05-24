# authentication_app/api/urls.py
from django.urls import path
from rest_framework import routers
from .views import UserVerifyAPIView, UserView, RegistrationViewSet, LoginView, PasswordRecoveryAPIView, ActivateUserAPIView



router = routers.DefaultRouter()

router.register(r'registration', RegistrationViewSet, basename='user-registration')

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('recovery-password/', PasswordRecoveryAPIView.as_view(), name='recovery-password'),
    path('verify/', UserVerifyAPIView.as_view(), name='user-verify'),
    path('user/', UserView.as_view(), name='user-view'),
    path('activate/<uidb64>/<token>/', ActivateUserAPIView.as_view(), name='user-activate'),
]

urlpatterns += router.urls