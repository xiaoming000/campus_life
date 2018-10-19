# Generated by Django 2.1.2 on 2018-10-19 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20181019_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='msgpost',
            name='id',
        ),
        migrations.AlterField(
            model_name='msgpost',
            name='message',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.Message'),
        ),
    ]