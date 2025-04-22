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
from rest_framework.response import Response
from rest_framework import status
from ..models import Video



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
            pass
        else:
            queryset = queryset.filter(profile__user=self.request.user)
        
        profile_id = self.request.query_params.get('profile')
        if profile_id is not None:
            queryset = queryset.filter(profile=profile_id)
        
        id_param = self.request.query_params.get('id')
        if id_param is not None:
            queryset = queryset.filter(id=id_param)
        
        return queryset
    

    @action(detail=True, methods=['get'], url_path='favorite-video-ids', permission_classes=[IsAuthenticated])
    def favorite_video_ids(self, request, pk=None):
        ids = list(self.get_object().favouriteVideos.values_list('id', flat=True))
        return Response(ids, status=status.HTTP_200_OK)


    
    @action(detail=True, methods=["post"], url_path="add-favorite", permission_classes=[IsAuthenticated, IsOwner])
    def add_favorite(self, request, pk=None):
        subprofile = self.get_object()
        video_id = request.data.get("video_id")

        if video_id is None:
            return Response(
                {"error": "video_id wird benötigt."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response(
                {"error": "Video nicht gefunden."},
                status=status.HTTP_404_NOT_FOUND
            )

        if subprofile.favouriteVideos.filter(pk=video_id).exists():
            subprofile.favouriteVideos.remove(video)
            return Response(
                {"video_id": video_id, "favorited": False},
                status=status.HTTP_200_OK
            )

        subprofile.favouriteVideos.add(video)
        return Response(
            {"video_id": video_id, "favorited": True},
            status=status.HTTP_201_CREATED
        )
