from django.apps import AppConfig


class ProfilAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_app'

    def ready(self):
        import profile_app.api.signals