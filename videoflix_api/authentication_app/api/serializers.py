from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework import status
from authentication_app.models import CustomUser


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
                'email': 'Diese E-Mail-Adresse ist bereits registriert.'
            })
        
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError({
                'username': 'Dieser Nutzername ist bereits registriert.'
            })

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', '')
        )
        return user



    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            address=validated_data['address']
        )
        return user












class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attributes):
        username = attributes.get('username')
        password = attributes.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Falsche Anmeldeinformationen oder ungültige Eingabe.', status.HTTP_400_BAD_REQUEST)

        attributes['user'] = user
        return attributes