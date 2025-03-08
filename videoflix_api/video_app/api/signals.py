import os
from django.dispatch import receiver
from video_app.models import Video
from django.db.models.signals import post_save, post_delete
from video_app.api.tasks import convert_to_480p
import django_rq # type: ignore

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert.')
    if created:
        print('Neues Video wurde erstellt.')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_to_480p, instance.video_file.path)    # rq worker server muss gestartet sein
        


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('Video-Datei wurde gelöscht.')