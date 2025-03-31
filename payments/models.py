from django.db import models
from django.contrib.auth.models import User

class UserEarnings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - ${self.balance}"

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payout_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Failed", "Failed")], default="Pending")

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.status}"

class WithdrawalRequest(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.creator.username} requested ${self.amount}"
    

# from django.db import models
# from users.models import Profile
# from django.contrib.auth.models import User


# class Transaction(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

#     def __str__(self):
#         return f"{self.user.user.username} - {self.amount}"


# class Earnings(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.ForeignKey(
#         "content.Content",
#         on_delete=models.CASCADE,
#         related_name="content_earnings"  # ✅ Fix by adding a unique related_name
#     )
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)

# class Withdrawal(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)


# class WithdrawalRequest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     method = models.CharField(max_length=50, choices=[("Bank", "Bank Transfer"), ("PayPal", "PayPal")])
#     status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed")], default="Pending")
#     requested_at = models.DateTimeField(auto_now_add=True)

