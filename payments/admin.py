from django.contrib import admin
from .models import Withdrawal, UserEarnings, WithdrawalRequest

# Register your models here.

admin.site.register(Withdrawal)
admin.site.register(UserEarnings)
admin.site.register(WithdrawalRequest)


# from .models import Transaction, Earnings, WithdrawalRequest

# # Register your models here.

# admin.site.register(Transaction)
# admin.site.register(Earnings)
# admin.site.register(WithdrawalRequest)
