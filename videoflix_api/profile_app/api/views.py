# profile_app/api/views.py

import mimetypes
import os
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profile_app.models import Profile, SubProfile
from core.ftp_client import FTPClient
from .permissions import IsOwner
from .serializers import ProfileSerializer, SubProfileSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status


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
    



class ProfilePictureUploadView(APIView):
    """
    API-View zum Hochladen eines Profilbildes.
    Erwartet eine Datei im 'file'-Feld des multipart/form-data Requests.
    """
    def post(self, request):
        # Extrahiere die hochgeladene Datei aus dem Request
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "Keine Datei übermittelt."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Optional: Generiere einen eindeutigen Remote-Pfad, z.B. unter Verwendung der User-ID oder eines Timestamps
        remote_path = os.path.join("profile_pics", file_obj.name)
        
        ftp_client = FTPClient()
        try:
            # Übertrage den Datei-Stream an den FTP-Server
            ftp_client.connection.storbinary(f"STOR {remote_path}", file_obj)
        except Exception as e:
            ftp_client.close()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        ftp_client.close()
        return Response({"message": "Upload erfolgreich"}, status=status.HTTP_200_OK)


class ProfilePictureDownloadView(APIView):
    """
    API-View zum Herunterladen eines Profilbildes.
    Der Dateiname wird als URL-Parameter erwartet.
    """
    def get(self, request, filename):
        remote_path = os.path.join("profile_pics", filename)
        ftp_client = FTPClient()
        try:
            # Lade die Datei in einen Buffer
            buffer = ftp_client.download_file_to_buffer(remote_path)
            ftp_client.close()
            # Bestimme den MIME-Typ der Datei
            content_type, _ = mimetypes.guess_type(filename)
            if not content_type:
                content_type = "application/octet-stream"
            
            response = HttpResponse(buffer, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            ftp_client.close()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

