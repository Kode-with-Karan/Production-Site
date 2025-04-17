from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from users.models import Profile

class PayPalTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paypal_order_id = models.CharField(max_length=255)
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    # In models.py of payments app
class Withdrawal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=20, default="Pending")  # or "Completed", "Failed"
    created_at = models.DateTimeField(auto_now_add=True)

class CreatorEarnings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_earned = models.FloatField(default=0)
    available_balance = models.FloatField(default=0)