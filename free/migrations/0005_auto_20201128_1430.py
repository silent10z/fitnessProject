# Generated by Django 3.0.2 on 2020-11-28 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('free', '0004_free_mainphoto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='free',
            old_name='mainphoto',
            new_name='photo',
        ),
    ]
