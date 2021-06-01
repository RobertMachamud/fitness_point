# Generated by Django 3.1.7 on 2021-05-03 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.TextField()),
                ('name', models.CharField(max_length=254)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('discount', models.BooleanField(blank=True, default=False, null=True)),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('duration_days', models.CharField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]
