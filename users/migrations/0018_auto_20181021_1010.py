# Generated by Django 2.1.2 on 2018-10-21 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20181020_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailnotification',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
