from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('authentication_app.api.urls')),
    path('api/video/', include('video_app.api.urls')),
    path('api/profile/', include('profile_app.api.urls')),
] + staticfiles_urlpatterns()

#  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]