# Generated by Django 3.0.2 on 2020-11-28 05:56

from django.db import migrations, models
import free.models


class Migration(migrations.Migration):

    dependencies = [
        ('free', '0005_auto_20201128_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='free',
            name='photo',
        ),
        migrations.AddField(
            model_name='free',
            name='filename',
            field=models.CharField(max_length=64, null=True, verbose_name='첨부파일명'),
        ),
        migrations.AddField(
            model_name='free',
            name='upload_files',
            field=models.FileField(blank=True, null=True, upload_to=free.models.get_file_path, verbose_name='파일'),
        ),
    ]
