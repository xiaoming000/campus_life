# Generated by Django 2.1.2 on 2018-10-19 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20181013_1849'),
        ('users', '0005_auto_20181019_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='post',
            field=models.ManyToManyField(blank=True, to='post.Post'),
        ),
    ]