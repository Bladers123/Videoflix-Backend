from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from .serializers import CustomUserSerializer, RegistrationSerializer, LoginSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from authentication_app.models import CustomUser
from rest_framework.throttling import AnonRateThrottle
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics
from .serializers import EmailSerializer




class UserViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

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
                'message': 'Erfolgreiche Registrierung',
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
                'message': 'Erfolgreiche Anmeldung',
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
                'successfully': True
            },
            status=status.HTTP_200_OK
        )
    



class SendEmailAPIView(generics.CreateAPIView):
    serializer_class = EmailSerializer

    def perform_create(self, serializer):
        # Hier würdest du das Versenden der Mail aufrufen
        data = serializer.validated_data
        subject = data['subject']
        message = data['message']
        recipient_list = data['recipient_list']
        from_email = data.get('from_email', None)
        # E-Mail-Versand logik...

    def post(self, request, format=None):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            subject = data['subject']
            message = data['message']
            recipient_list = data['recipient_list']
            from_email = data.get('from_email', getattr(settings, 'DEFAULT_FROM_EMAIL'))
            
            if from_email is None:
                return Response(
                    {"detail": "Kein Absender definiert. Gib 'from_email' an oder setze DEFAULT_FROM_EMAIL in settings."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                return Response(
                    {"detail": f"Fehler beim Versenden der E-Mail: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response({"detail": "E-Mail erfolgreich versendet."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)