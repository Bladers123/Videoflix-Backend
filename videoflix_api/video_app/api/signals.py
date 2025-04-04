# video_app/api/signals.py
import os
from django.dispatch import receiver
from video_app.models import Video
from django.db.models.signals import post_save, post_delete
import django_rq # type: ignore


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert.')
    if created:
        print('Neues Video wurde erstellt.')
        queue = django_rq.get_queue('default', autocommit=True)
        
        


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('Video-Datei wurde gelöscht.')


