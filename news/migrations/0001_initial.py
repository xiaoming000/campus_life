# Generated by Django 2.1 on 2018-08-20 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField()),
                ('modified_time', models.DateTimeField()),
                ('delete', models.SmallIntegerField(default=0)),
                ('excerpt', models.CharField(blank=True, max_length=300)),
                ('views', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]
