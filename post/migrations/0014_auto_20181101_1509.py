# Generated by Django 2.1 on 2018-11-01 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20181101_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]