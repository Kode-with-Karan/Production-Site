# Generated by Django 5.1.3 on 2025-02-07 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('content_type', models.CharField(choices=[('short_film', 'Short Film'), ('podcast', 'Podcast'), ('documentary', 'Documentary'), ('entertainment', 'Entertainment Project')], max_length=50)),
                ('file', models.FileField(upload_to='content_files/')),
                ('thumbnail', models.ImageField(blank=True, upload_to='content_thumbnails/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('earnings', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
