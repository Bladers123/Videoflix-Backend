# video_app/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, Http404
from core.ftp_client import FTPClient
import os




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



class VideoNameView(APIView):
    throttle_classes = []
    def get(self, request):
        try:
            ftp_client = FTPClient()
            video_titles = ftp_client.list_video_titles()
            ftp_client.close()
            return Response(video_titles)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
