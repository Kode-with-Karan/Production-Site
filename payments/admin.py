from django.contrib import admin
# from .models import Withdrawal, UserEarnings, WithdrawalRequest
from .models import PayPalTransaction, Withdrawal, CreatorEarnings

# Register your models here.

admin.site.register(PayPalTransaction)
admin.site.register(Withdrawal)
admin.site.register(CreatorEarnings)

# from .models import Transaction, Earnings, WithdrawalRequest

# # Register your models here.

# admin.site.register(Transaction)
# admin.site.register(Earnings)
# admin.site.register(WithdrawalRequest)
