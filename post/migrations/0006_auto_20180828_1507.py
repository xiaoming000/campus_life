# Generated by Django 2.1 on 2018-08-28 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_postreply_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='postreply',
            name='reply_type',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='postreply',
            name='reply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.PostReply'),
        ),
    ]
