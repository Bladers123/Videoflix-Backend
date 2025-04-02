# video_app/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, Http404
from core.ftp_client import FTPClient




class DownloadVideoView(APIView):
    def get(self, request, video_name):
        # Hier gehen wir davon aus, dass das HLS-Manifest mit der Endung .m3u8 vorliegt
        remote_path = f'/videos/{video_name}'
        try:
            ftp_client = FTPClient()
            buffer = ftp_client.download_file_to_buffer(remote_path)
            ftp_client.close()
        except Exception as e:
            raise Http404(f"Fehler beim Abrufen der Datei: {e}")
        
        # Für m3u8-Dateien wird als MIME-Typ 'application/vnd.apple.mpegurl' genutzt
        response = StreamingHttpResponse(buffer, content_type='application/vnd.apple.mpegurl')
        # Wenn der Stream direkt im Browser abgespielt werden soll, ist Content-Disposition in der Regel nicht nötig.
        return response




class VideoTestView(APIView):
    def get(self, request, format=None):
        return Response({'message': 'Test View der Video App'})