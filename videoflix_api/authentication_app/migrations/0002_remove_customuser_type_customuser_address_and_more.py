# Generated by Django 5.1.6 on 2025-03-08 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='type',
        ),
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='customuser',
            name='custom',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default='', max_length=25),
        ),
    ]
