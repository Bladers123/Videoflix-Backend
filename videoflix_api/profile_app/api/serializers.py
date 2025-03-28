# profile_app/api/serializers.py
from ftplib import error_perm
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
        # Deine bisherigen Validierungen...
        password = data.get('password')
        if password and password.strip():
            if len(password) < 8:
                raise serializers.ValidationError({"password": "Passwort muss mindestens 8 Zeichen lang sein"})

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
        image_file = validated_data.get('img', None)
        if image_file:
            image_file.seek(0)
            from core.ftp_client import FTPClient
            ftp_client = FTPClient()
            ftp_conn = ftp_client.connection

            remote_directory = f"profile_images/{instance.id}"
            parts = remote_directory.split('/')
            current_path = ""
            from ftplib import error_perm
            for part in parts:
                if part:
                    current_path = f"{current_path}/{part}" if current_path else part
                    try:
                        ftp_conn.mkd(current_path)
                    except error_perm as e:
                        if not str(e).startswith("550"):
                            raise
            remote_path = f"/profile_images/{instance.id}/{image_file.name}"
            ftp_conn.storbinary(f"STOR {remote_path}", image_file)
            ftp_client.close()
            validated_data['img'] = remote_path

        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            user = instance.user
            user.set_password(password)
            user.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        img = representation.get('img')
        if img:
            request = self.context.get('request')
            if img.startswith("http://") or img.startswith("https://"):
                if "profile_images/" in img:
                    relative_path = img.split("profile_images/", 1)[1]
                    relative_path = f"profile_images/{relative_path}"
                else:
                    relative_path = img
            else:
                relative_path = img
            ftp_image_url = request.build_absolute_uri(
                f"/api/profile/ftp-images/{relative_path}"
            ) if request else f"/api/profile/ftp-images/{relative_path}"
            representation['img'] = ftp_image_url
            print(ftp_image_url)
        return representation







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



   
        