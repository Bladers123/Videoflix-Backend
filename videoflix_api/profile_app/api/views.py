# profile_app/api/views.py

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profile_app.models import Profile, SubProfile
from .permissions import IsOwner
from .serializers import ProfileSerializer, SubProfileSerializer
from rest_framework import viewsets


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer




class SubProfileViewSet(viewsets.ModelViewSet):
    queryset = SubProfile.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = SubProfileSerializer
        

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.user.is_superuser:
            # Admins bekommen alle Ergebnisse
            pass
        else:
            queryset = queryset.filter(profile__user=self.request.user)
        
        # Filter, falls ein Query-Parameter 'profile' vorhanden ist (für andere Endpunkte)
        profile_id = self.request.query_params.get('profile')
        if profile_id is not None:
            queryset = queryset.filter(profile=profile_id)
        
        # Neuen Filter für den Query-Parameter 'id' hinzufügen
        id_param = self.request.query_params.get('id')
        if id_param is not None:
            queryset = queryset.filter(id=id_param)
        
        return queryset


