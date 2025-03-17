from rest_framework import serializers
from profile_app.models import Profile, SubProfile



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'user',
            'username',
            'first_name',
            'last_name',
            'address',
            'phone',
            'email'
        )


class SubProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubProfile
        fields = (
            'profile',
            'name',
            'img'
        )