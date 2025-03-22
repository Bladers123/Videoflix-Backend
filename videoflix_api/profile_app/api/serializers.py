from rest_framework import serializers
from profile_app.models import Profile, SubProfile



class ProfileSerializer(serializers.ModelSerializer):
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
            'email'
        )


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



   
        