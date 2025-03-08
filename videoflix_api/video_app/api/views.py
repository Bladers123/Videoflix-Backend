# video_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, Http404
from core.ftp_client import FTPClient




class StreamVideoView(APIView):
    def get(self, request, video_name):
        remote_path = f'/videos/{video_name}.mp4'
        try:
            ftp_client = FTPClient()
            buffer = ftp_client.download_file_to_buffer(remote_path)
            ftp_client.close()
        except Exception as e:
            raise Http404(f"Fehler beim Abrufen der Datei: {e}")
        
        response = StreamingHttpResponse(buffer, content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{video_name}.mp4"'
        return response



class VideoTestView(APIView):
    def get(self, request, format=None):
        return Response({'message': 'Test View der Video App'})