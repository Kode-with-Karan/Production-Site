# Generated by Django 5.1.3 on 2025-02-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_last_payment_profile_total_earnings_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_account_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
