from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileTestView(APIView):
    def get(self, request, format=None):
        return Response({'message': 'Test View der Profile App'})
