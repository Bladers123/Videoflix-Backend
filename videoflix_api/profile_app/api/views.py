# profile_app/api/views.py

import mimetypes
import os
from django.http import Http404, HttpResponse
from rest_framework.permissions import IsAuthenticated
from profile_app.models import Profile, SubProfile
from core.ftp_client import FTPClient
from .permissions import IsOwner
from .serializers import ProfileSerializer, SubProfileSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

def serve_ftp_image(request, image_path):
    if not image_path.startswith("/"):
        image_path = "/" + image_path

    ftp_client = FTPClient()
    try:
        buffer = ftp_client.download_file_to_buffer(image_path)
    except Exception:
        ftp_client.close()
        raise Http404("Bild nicht gefunden")
    ftp_client.close()

    content_type, _ = mimetypes.guess_type(image_path)
    if not content_type:
        content_type = 'application/octet-stream'
    
    response = HttpResponse(buffer.read(), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(image_path)}"'
    return response







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
    
    
    @action(detail=True, methods=["post"], url_path="add-favorite", permission_classes=[IsAuthenticated, IsOwner])
    def add_favorite(self, request, pk=None):
        """
        Fügt ein Video per POST als Favoriten zum SubProfile hinzu.
        Erwartet im Body ein JSON mit 'video_id'.
        """
        subprofile = self.get_object()
        video_id = request.data.get("video_id")

        if not video_id:
            return Response({"error": "video_id wird benötigt."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({"error": "Video nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)

        subprofile.favouriteVideos.add(video)
        # Optional: Rückgabe des aktualisierten Favoriten-Arrays oder eines Status-Messages.
        return Response({"status": "Video wurde zu den Favoriten hinzugefügt."}, status=status.HTTP_201_CREATED)