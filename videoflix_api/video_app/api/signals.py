# video_app/api/signals.py
import os
from django.dispatch import receiver
from video_app.models import Video
from django.db.models.signals import post_save, post_delete
import django_rq  # type: ignore
from .tasks import convert_to_1080p, convert_to_120p, convert_to_360p, convert_to_720p, delete_local_media_folder, upload_master_playlist, upload_hls_files, upload_thumbnail



@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    queue = django_rq.get_queue('default', autocommit=True)
    directory, filename = os.path.split(instance.video_file.path)
    name, ext = os.path.splitext(filename)
    video_type = instance.video_type

    job120 = queue.enqueue(convert_to_120p, instance.video_file.path)
    job360 = queue.enqueue(convert_to_360p, instance.video_file.path)
    job720 = queue.enqueue(convert_to_720p, instance.video_file.path)
    job1080 = queue.enqueue(convert_to_1080p, instance.video_file.path)

    job_hls = queue.enqueue(upload_hls_files, directory, name, video_type, depends_on=[job120, job360, job720, job1080])

    job_master = queue.enqueue(upload_master_playlist, directory, name, name, video_type, depends_on=job_hls)

    if instance.thumbnail:
        thumb_dir, thumb_filename = os.path.split(instance.thumbnail.path)
        thumb_name, thumb_ext = os.path.splitext(thumb_filename)
        video_folder = thumb_name

        job_thumb = queue.enqueue(
            upload_thumbnail,
            instance.thumbnail.path,
            video_folder,
            instance.video_type,
            thumb_filename,
            depends_on=job_master
        )
        queue.enqueue(delete_local_media_folder, depends_on=job_thumb)
    else:
        queue.enqueue(delete_local_media_folder, depends_on=job_master)

    if instance.video_file:
        Video.objects.filter(pk=instance.pk).update(file_size=instance.video_file.size)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('Video-Datei wurde gelöscht.')
