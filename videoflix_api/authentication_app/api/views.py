# authentication_app/api/views.py
from rest_framework.viewsets import GenericViewSet
from .serializers import CustomUserSerializer, RegistrationSerializer, LoginSerializer, PasswordRecoverySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from authentication_app.models import CustomUser
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.conf import settings


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            
            serializer = CustomUserSerializer(request.user)
            user = serializer.data
            return Response({
                'message': 'Laden war erfolgreich.',
                'token': user['auth_token'],
                'username': user['username'],
                'email': user['email'],
                'id': user['id'],
                'successfully': True,
                'profile': user['profile'] 
            }, status=status.HTTP_200_OK)


class RegistrationViewSet(CreateModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    throttle_classes = [AnonRateThrottle]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'Registrierung war erfolgreich.',
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
                'successfully': True
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'Login war erfolgreich.',
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'id': user.id,
                'successfully': True,
                'profile': user.profile.id
            },
            status=status.HTTP_200_OK
        )


class PasswordRecoveryAPIView(generics.CreateAPIView):
    serializer_class = PasswordRecoverySerializer

    def perform_create(self, serializer):
        serializer.save() 
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                'message': 'Senden war erfolgreich.',
                'successfully': True
            },
            status=status.HTTP_200_OK
        )



class UserVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user 
        if user:
            return Response(
                {
                    'exists': True, 
                    'username': user.username
                },
                status=status.HTTP_200_OK)
        
        return Response({'exists': False}, status=status.HTTP_401_UNAUTHORIZED)



class ActivateUserAPIView(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        # decodieren & prüfen
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return redirect(
                f"{settings.FORWARDING_URL}/#/activate/{uidb64}/{token}?success=false"
            )

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(
                f"{settings.FORWARDING_URL}/#/activate/{uidb64}/{token}?success=true"
            )
        else:
            return redirect(
                f"{settings.FORWARDING_URL}/#/activate/{uidb64}/{token}?success=false"
            )