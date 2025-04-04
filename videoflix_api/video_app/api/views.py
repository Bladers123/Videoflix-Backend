# video_app/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, Http404
from core.ftp_client import FTPClient




class DownloadVideoView(APIView):
    def get(self, request, video_name, file_name=None):
        # Falls kein file_name übergeben wird, liefern wir das Manifest
        if file_name is None:
            remote_path = f'/videos/{video_name}/{video_name}.m3u8'
            content_type = 'application/vnd.apple.mpegurl'
        else:
            remote_path = f'/videos/{video_name}/{file_name}'
            # MIME-Typ anhand der Dateiendung festlegen
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




class VideoTestView(APIView):
    def get(self, request, format=None):
        return Response({'message': 'Test View der Video App'})