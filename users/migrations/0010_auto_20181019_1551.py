# Generated by Django 2.1.2 on 2018-10-19 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_message_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='category',
        ),
        migrations.RemoveField(
            model_name='message',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='to_user',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
