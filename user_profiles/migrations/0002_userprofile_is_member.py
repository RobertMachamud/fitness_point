# Generated by Django 3.1.7 on 2021-05-03 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_member',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]