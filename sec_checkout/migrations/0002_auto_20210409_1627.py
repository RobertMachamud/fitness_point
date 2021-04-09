# Generated by Django 3.1.7 on 2021-04-09 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sec_checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderlineitem',
            old_name='offer_sz',
            new_name='item_sz',
        ),
        migrations.AddField(
            model_name='order',
            name='original_cart',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_pid',
            field=models.CharField(default='', max_length=254),
        ),
    ]