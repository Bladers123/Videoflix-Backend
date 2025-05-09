# Generated by Django 5.1.6 on 2025-04-13 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0004_profile_img'),
        ('video_app', '0006_video_video_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='subprofile',
            name='favouriteVideos',
            field=models.ManyToManyField(blank=True, related_name='subprofile_favorites', to='video_app.video'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
