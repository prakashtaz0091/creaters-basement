# Generated by Django 3.2.4 on 2021-08-02 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210802_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalAudio',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('file', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.audiofile')),
            ],
        ),
    ]
