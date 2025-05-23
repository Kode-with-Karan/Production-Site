# Generated by Django 5.1.3 on 2025-02-12 01:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_content_cast_content_country_content_duration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='content_images/')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='content.content')),
            ],
        ),
    ]
