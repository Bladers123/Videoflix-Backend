
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profile_app.models import Profile, SubProfile
from .serializers import ProfileSerializer, SubProfileSerializer
from rest_framework import viewsets


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer


class SubProfileViewSet(viewsets.ModelViewSet):
    queryset = SubProfile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubProfileSerializer

    