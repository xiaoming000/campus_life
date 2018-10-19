# Generated by Django 2.1.2 on 2018-10-08 21:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0007_auto_20180828_1735'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostComent',
            new_name='PostComment',
        ),
        migrations.RenameField(
            model_name='postreply',
            old_name='post_comment',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='postreply',
            old_name='reply',
            new_name='comment_reply',
        ),
        migrations.RenameField(
            model_name='postreply',
            old_name='content',
            new_name='text',
        ),
    ]
