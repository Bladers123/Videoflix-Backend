# authentication_app/api/urls.py
from django.urls import path
from rest_framework import routers
from .views import UserVerifyAPIView, UserView, RegistrationViewSet, LoginView, PasswordRecoveryAPIView

router = routers.DefaultRouter()


router.register(r'registration', RegistrationViewSet, basename='user-registration')

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('recovery-password/', PasswordRecoveryAPIView.as_view(), name='recovery-password'),
    path('verify/', UserVerifyAPIView.as_view(), name='user-verify'),
    path('user/', UserView.as_view(), name='user-view')

]

urlpatterns += router.urls