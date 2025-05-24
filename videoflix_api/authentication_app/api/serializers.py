# authentication_app/api/serilizers.py
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework import status
from authentication_app.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            field.name
            for field in CustomUser._meta.get_fields()
            if not field.is_relation or field.one_to_one or field.many_to_one
        ] 

  

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(
        write_only=True,
        error_messages={'blank': 'Bitte das [Passwort wiederholen] Feld ausfüllen.'}
    )
    username = serializers.CharField(
        error_messages={'blank': 'Bitte das [Nutzername] Feld ausfüllen.'}
    )
    email = serializers.EmailField(
        error_messages={'blank': 'Bitte das [Email] Feld ausfüllen.'}
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={'blank': 'Bitte das [Passwort] Feld ausfüllen.'}
    )

    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'password', 'repeated_password',
            'phone', 'address', 'first_name', 'last_name',
        )

    def validate(self, data):
        password = data.get('password')
        repeated_password = data.get('repeated_password')
        email = data.get('email')
        username = data.get('username')

        if password != repeated_password:
            raise serializers.ValidationError({
                'repeated_password': 'Passwörter stimmen nicht überein.'
            })
        
        if len(password) < 8:
            raise serializers.ValidationError({
                'password': 'Passwort muss mindestens 8 Zeichen lang sein.'
            })

        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({
                'email': 'Bitte überprüfe deine Eingaben und versuche es erneut.'
            })
        
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError({
                'username': 'Dieser Nutzername ist bereits registriert.'
            })

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(
            username  = validated_data['username'],
            email     = validated_data['email'],
            password  = validated_data['password'],
            is_active = False,
            # … weitere Felder …
        )

        # UID & Token
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token  = default_token_generator.make_token(user)

        # Basis-URL aus settings + Aktivierungspfad
        # Achte darauf, ob REGISTRATION_EMAIL_URL schon mit Slash endet
        base_url = settings.REGISTRATION_EMAIL_URL.rstrip('/')
        activation_link = f"{base_url}/auth/activate/{uidb64}/{token}/"

        subject = "Aktiviere Dein Videoflix-Konto"
        message = (
            f"Hallo {user.username},\n\n"
            "klicke bitte auf den folgenden Link, um Dein Konto zu aktivieren:\n\n"
            f"{activation_link}\n\n"
            "Viele Grüße\n"
            "Dein Videoflix-Team"
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [user.email])

        return user





class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Bitte das [Email] Feld ausfüllen.',
            'blank': 'Bitte das [Email] Feld ausfüllen.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'Bitte das [Passwort] Feld ausfüllen.',
            'blank': 'Bitte das [Passwort] Feld ausfüllen.'
        }
    )

    def validate(self, attributes):
        email = attributes.get('email')
        password = attributes.get('password')

        try:
            user_instance = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Falsche Anmeldeinformationen oder ungültige Eingabe.', status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=user_instance.username, password=password)

        if not user:
            raise AuthenticationFailed('Falsche Anmeldeinformationen oder ungültige Eingabe.', status.HTTP_400_BAD_REQUEST)

        attributes['user'] = user
        return attributes



class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Bitte das [Email] Feld ausfüllen.',
            'blank':    'Bitte das [Email] Feld ausfüllen.',
            'invalid':  'Bitte eine gültige E-Mail-Adresse eingeben.'
        }
    )

    def create(self, validated_data):
        email = validated_data['email']
        try:
            user = CustomUser.objects.get(email__iexact=email)
        except CustomUser.DoesNotExist:
            user = None

        if user:
            random_password = get_random_string(length=8)
            user.set_password(random_password)
            user.save()

            subject = "Passwort zurücksetzen"
            message = (
                f"Dein neues Passwort lautet: {random_password}\n"
                "Im Dashboard kannst du das Passwort ändern.\n\n"
                "Mit freundlichen Grüßen\n"
                "Dein Videoflix Team"
            )
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
            if not from_email:
                raise serializers.ValidationError(
                    'Interner Serverfehler: Absenderadresse nicht konfiguriert.'
                )
            send_mail(subject, message, from_email, [email])

        return {'detail': 'Wenn eine Übereinstimmung gefunden wurde, hast du gleich Post.'}
