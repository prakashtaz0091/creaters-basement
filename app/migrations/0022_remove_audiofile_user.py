# Generated by Django 3.2.4 on 2021-08-04 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_audiofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofile',
            name='user',
        ),
    ]
