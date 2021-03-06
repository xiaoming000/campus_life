# Generated by Django 2.1 on 2018-11-01 15:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0012_postcollect_postlike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcollect',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postcollect',
            name='user',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='user',
        ),
        migrations.AddField(
            model_name='post',
            name='collects',
            field=models.ManyToManyField(blank=True, related_name='collects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='PostCollect',
        ),
        migrations.DeleteModel(
            name='PostLike',
        ),
    ]
