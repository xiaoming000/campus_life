# Generated by Django 2.1 on 2018-08-20 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField()),
                ('modified_time', models.DateTimeField()),
                ('delete', models.SmallIntegerField(default=0)),
                ('excerpt', models.CharField(blank=True, max_length=300)),
                ('anonym', models.SmallIntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('auther', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Category')),
                ('tags', models.ManyToManyField(blank=True, to='users.Tag')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]
