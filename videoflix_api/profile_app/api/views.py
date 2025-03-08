
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profile_app.models import Profile
from .serializers import ProfileSerializer
from rest_framework import viewsets


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
