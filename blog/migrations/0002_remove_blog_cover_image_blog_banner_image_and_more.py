# Generated by Django 5.1.3 on 2025-02-15 04:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='cover_image',
        ),
        migrations.AddField(
            model_name='blog',
            name='banner_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='blog_banners/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='main_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='blog_main/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='optional_image1',
            field=models.ImageField(blank=True, null=True, upload_to='blog_optional/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='optional_image2',
            field=models.ImageField(blank=True, null=True, upload_to='blog_optional/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='optional_image3',
            field=models.ImageField(blank=True, null=True, upload_to='blog_optional/'),
        ),
    ]
