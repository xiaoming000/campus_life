# Generated by Django 2.1 on 2018-08-28 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now_add=True)),
                ('delete', models.SmallIntegerField(default=0)),
                ('excerpt', models.CharField(blank=True, max_length=300)),
                ('anonym', models.SmallIntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='PostComent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('delete', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PostReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('delete', models.SmallIntegerField(default=0)),
                ('post_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.PostComent')),
                ('reply', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='post.PostReply')),
            ],
        ),
    ]
