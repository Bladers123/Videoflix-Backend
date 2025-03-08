from django.contrib import admin
from .models import Video
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore



class VideoResource(resources.ModelResource):
    class Meta:
        model = Video 


class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource


admin.site.register(Video, VideoAdmin)