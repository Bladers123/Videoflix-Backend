from django.urls import path
from rest_framework import routers
from .views import UserViewSet, RegistrationViewSet, LoginView, PasswordRecoveryAPIView

router = routers.DefaultRouter()

router.register(r'user', UserViewSet, basename='user-auth')
router.register(r'registration', RegistrationViewSet, basename='user-registration')

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('recovery-password/', PasswordRecoveryAPIView.as_view(), name='recovery-password'),

]

urlpatterns += router.urls