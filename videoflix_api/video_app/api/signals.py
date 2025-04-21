# video_app/api/signals.py
import os
from django.dispatch import receiver
from video_app.models import Video
from django.db.models.signals import post_save, post_delete
import django_rq # type: ignore
from .tasks import  convert_to_1080p, convert_to_120p, convert_to_360p, convert_to_720p, generate_and_upload_master_playlist, upload_hls_files



@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert.')
    if created:
        print('Neues Video wurde erstellt.')
        queue = django_rq.get_queue('default', autocommit=True)
        
        directory, filename = os.path.split(instance.video_file.path)
        name, ext = os.path.splitext(filename)
        video_type = instance.video_type

        queue.enqueue(convert_to_120p, instance.video_file.path)
        queue.enqueue(convert_to_360p, instance.video_file.path)
        queue.enqueue(convert_to_720p, instance.video_file.path)
        queue.enqueue(convert_to_1080p, instance.video_file.path)
        queue.enqueue(upload_hls_files, directory, name, video_type)
        queue.enqueue(generate_and_upload_master_playlist, directory, name, name, video_type)
        print('Videos sind fertig hochgeladen.')

        if instance.video_file:
            Video.objects.filter(pk=instance.pk).update(
                file_size=instance.video_file.size
            )
            print(f"Dateigröße ({instance.video_file.size} Bytes) in DB gespeichert.")


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('Video-Datei wurde gelöscht.')