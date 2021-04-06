# Generated by Django 3.1.7 on 2021-04-06 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='offer',
            name='has_sizes',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='is_shoe',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
