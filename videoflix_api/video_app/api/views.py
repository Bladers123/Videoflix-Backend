# video_app/api/views.py
import mimetypes
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework.response import Response
from django.http import HttpResponse, StreamingHttpResponse, Http404
from core.ftp_client import FTPClient
import os
from rest_framework.permissions import IsAuthenticated

from .serializers import VideoSerializer
from ..models import Video

def serve_ftp_image(request, image_path):
        """
        Generisches FTP-Image-Serving, z.B. für
        /api/video/ftp-images/clips/<folder>/<file>
        """
        # führenden Slash sicherstellen
        remote_path = image_path if image_path.startswith("/") else f"/{image_path}"

        ftp = FTPClient()
        try:
            buffer = ftp.download_file_to_buffer(remote_path)
        except Exception:
            ftp.close()
            raise Http404(f"Bild nicht gefunden: {remote_path}")
        finally:
            ftp.close()

        content_type, _ = mimetypes.guess_type(remote_path)
        content_type = content_type or "application/octet-stream"

        return HttpResponse(buffer.read(), content_type=content_type)



class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    throttle_classes = [] 
    
    def get_serializer_context(self):
        return {'request': self.request}




class DownloadVideoView(APIView):
    throttle_classes = []
    def get(self, request, video_type, video_name, file_path=None):
        if video_type == 'movie':
            base_path = '/movies'
        elif video_type == 'clip':
            base_path = '/clips'
        else:
            raise Http404("Unbekannter Video-Typ")

        if file_path is None:
            remote_path = f'{base_path}/{video_name}/master.m3u8'
            content_type = 'application/vnd.apple.mpegurl'
        else:
            file_name = os.path.basename(file_path)
            remote_path = f'{base_path}/{video_name}/{file_name}'
            if file_name.endswith('.ts'):
                content_type = 'video/MP2T'
            else:
                content_type = 'application/octet-stream'
                
        print(remote_path)
        try:
            ftp_client = FTPClient()
            buffer = ftp_client.download_file_to_buffer(remote_path)
            ftp_client.close()
        except Exception as e:
            raise Http404(f"Fehler beim Abrufen der Datei: {e}")
        
        return StreamingHttpResponse(buffer, content_type=content_type)




        


