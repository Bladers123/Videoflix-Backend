from rest_framework.views import APIView
from rest_framework.response import Response

class VideoTestView(APIView):
    def get(self, request, format=None):
        return Response({'message': 'Test View der Video App'})
