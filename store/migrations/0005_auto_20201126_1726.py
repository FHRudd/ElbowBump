# Generated by Django 3.0.7 on 2020-11-26 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20201126_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='variant',
        ),
        migrations.RemoveField(
            model_name='variants',
            name='name',
        ),
    ]
