# Generated by Django 3.1.6 on 2021-03-13 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210311_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='GazeTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userTime', models.CharField(max_length=40)),
                ('userGaze', models.FloatField(max_length=40)),
                ('userStatus', models.IntegerField()),
                ('userCreateTime', models.CharField(max_length=40)),
                ('userNickName', models.CharField(default='unknown', max_length=40)),
                ('userDetectClass', models.CharField(default='unknown', max_length=40)),
            ],
        ),
    ]
