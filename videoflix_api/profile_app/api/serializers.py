# profile_app/api/serializers.py
from rest_framework import serializers
from profile_app.models import Profile, SubProfile



class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'subprofile',
            'username',
            'first_name',
            'last_name',
            'address',
            'phone',
            'email',
            'password',
            'img'
        )

    def validate(self, data):
        password = data.get('password')

        # Falls ein Passwortwert übergeben wird und nicht nur ein leerer String ist, führe die Validierung durch
        if password and password.strip():
            if len(password) < 8:
                raise serializers.ValidationError({"password": "Passwort muss mindestens 8 Zeichen lang sein"})

        # Weitere Feldvalidierungen:
        email = data.get('email')
        if email and '@' not in email:
            raise serializers.ValidationError({"email": "Ungültige E-Mail-Adresse"})

        phone = data.get('phone')
        if phone and len(phone) < 5:
            raise serializers.ValidationError({"phone": "Ungültige Telefonnummer"})

        address = data.get('address')
        if address and len(address) < 5:
            raise serializers.ValidationError({"address": "Ungültige Adresse"})

        first_name = data.get('first_name')
        if first_name and len(first_name) < 2:
            raise serializers.ValidationError({"first_name": "Ungültiger Vorname"})

        last_name = data.get('last_name')
        if last_name and len(last_name) < 2:
            raise serializers.ValidationError({"last_name": "Ungültiger Nachname"})

        username = data.get('username')
        if username and len(username) < 2:
            raise serializers.ValidationError({"username": "Ungültiger Benutzername"})

        return data
       

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            user = instance.user
            user.set_password(password)
            user.save()
        return instance



class SubProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubProfile
        fields = (
            'id',
            'profile',
            'name',
        )

    name = serializers.CharField(
        error_messages={
            'required': 'Bitte das [Name] Feld ausfüllen.',
            'blank': 'Bitte das [Name] Feld ausfüllen.'
        }
    )

    def validate(self, data):
        profile = data.get('profile')
        if profile:
            if self.instance:
                count = profile.subprofile.exclude(pk=self.instance.pk).count()
            else:
                count = profile.subprofile.count()
            if count >= 4:
                raise serializers.ValidationError({
                    '__all__': 'Es dürfen maximal 4 SubProfiles für dieses Profile existieren.'
                })
        return data



   
        