# Generated by Django 3.1.7 on 2021-05-30 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0003_userprofile_default_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='default_full_name',
        ),
    ]
