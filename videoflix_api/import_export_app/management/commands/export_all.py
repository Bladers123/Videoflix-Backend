import os
from django.core.management.base import BaseCommand
from django.conf import settings
from import_export import resources # type: ignore

# Modelle importieren
from video_app.models import Video
from profile_app.models import Profile
from authentication_app.models import CustomUser as User

# Ressourcen definieren
class VideoResource(resources.ModelResource):
    class Meta:
        model = Video

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class Command(BaseCommand):
    help = "Exportiert Daten aus Video, Profile und User in CSV- und JSON-Dateien"

    def handle(self, *args, **options):
        # Export-Ordner bestimmen und anlegen, falls nicht vorhanden.
        export_folder = os.path.join(settings.BASE_DIR, "import_export_app", "export_data")
        os.makedirs(export_folder, exist_ok=True)

        # Video-Daten exportieren
        video_resource = VideoResource()
        video_dataset = video_resource.export()
        video_csv = video_dataset.csv
        video_json = video_dataset.json
        with open(os.path.join(export_folder, 'videos_export.csv'), 'w', encoding='utf-8') as f:
            f.write(video_csv)
        with open(os.path.join(export_folder, 'videos_export.json'), 'w', encoding='utf-8') as f:
            f.write(video_json)
        self.stdout.write(self.style.SUCCESS("Video-Daten wurden erfolgreich exportiert."))

        # Profile-Daten exportieren
        profile_resource = ProfileResource()
        profile_dataset = profile_resource.export()
        profile_csv = profile_dataset.csv
        profile_json = profile_dataset.json
        with open(os.path.join(export_folder, 'profiles_export.csv'), 'w', encoding='utf-8') as f:
            f.write(profile_csv)
        with open(os.path.join(export_folder, 'profiles_export.json'), 'w', encoding='utf-8') as f:
            f.write(profile_json)
        self.stdout.write(self.style.SUCCESS("Profile-Daten wurden erfolgreich exportiert."))

        # User-Daten exportieren
        user_resource = UserResource()
        user_dataset = user_resource.export()
        user_csv = user_dataset.csv
        user_json = user_dataset.json
        with open(os.path.join(export_folder, 'users_export.csv'), 'w', encoding='utf-8') as f:
            f.write(user_csv)
        with open(os.path.join(export_folder, 'users_export.json'), 'w', encoding='utf-8') as f:
            f.write(user_json)
        self.stdout.write(self.style.SUCCESS("User-Daten wurden erfolgreich exportiert."))
