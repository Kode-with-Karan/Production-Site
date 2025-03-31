import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserEarnings, Withdrawal, WithdrawalRequest

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def withdraw_funds(request):
    user_earnings = UserEarnings.objects.get(user=request.user)
    
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        stripe_account = request.POST.get("stripe_account")  # User's Stripe account

        if amount < 10:
            messages.error(request, "Minimum withdrawal amount is $10.")
            return redirect("withdraw_funds")

        if amount > user_earnings.balance:
            messages.error(request, "Insufficient balance.")
            return redirect("withdraw_funds")

        try:
            # Create a Stripe Payout
            payout = stripe.Payout.create(
                amount=int(amount * 100),  # Convert to cents
                currency="usd",
                method="standard",
                destination=stripe_account,
            )

            # Deduct balance and store withdrawal record
            user_earnings.balance -= amount
            user_earnings.save()

            Withdrawal.objects.create(
                user=request.user,
                amount=amount,
                stripe_payout_id=payout.id,
                status="Completed",
            )

            messages.success(request, "Withdrawal successful. Funds will be processed shortly.")
            return redirect("withdraw_funds")

        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe Error: {str(e)}")

    return render(request, "payments/withdraw.html", {"balance": user_earnings.balance})

@login_required
def withdrawal_history(request):
    history = Withdrawal.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "payments/history.html", {"history": history})
@login_required
def transactions(request):
    history = Withdrawal.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "payments/history.html", {"history": history})
@login_required
def earnings(request):
    history = Withdrawal.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "payments/history.html", {"history": history})


def process_withdrawal(user, amount, destination_account):
    if amount < 10:
        return {"error": "Minimum withdrawal is $10"}

    earnings = UserEarnings.objects.get(user=user)

    if earnings.balance < amount:
        return {"error": "Insufficient balance"}

    try:
        transfer = stripe.Transfer.create(
            amount=int(amount * 100),  # Convert to cents
            currency="usd",
            destination=destination_account,  # The creator's Stripe account ID
        )

        # Deduct from the creator's balance
        earnings.balance -= amount
        earnings.save()

        # Mark withdrawal as completed
        WithdrawalRequest.objects.create(creator=user, amount=amount, status="Completed")
        
        return {"success": "Withdrawal processed successfully"}

    except stripe.error.StripeError as e:
        return {"error": str(e)}
    

@login_required
def request_withdrawal(request):
    earnings = UserEarnings.objects.get(user=request.user)
    print("Aaa gaya")
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        destination_account = request.POST.get("stripe_account")

        response = process_withdrawal(request.user, amount, destination_account)
        print(response)
        if "error" in response:
            print(response["error"])
            return render(request, "payments/withdraw.html", {"error": response["error"], "earnings": earnings})

        return redirect("withdrawal_success")

    return render(request, "payments/withdraw.html", {"earnings": earnings})

@login_required
def dashboard(request):
    earnings = UserEarnings.objects.get(user=request.user)
    return render(request, "payments/earning.html", {"earnings": earnings})

# from django.shortcuts import render
# from .models import Transaction, Withdrawal, Earnings
# from notifications.models import Notification
# from django.contrib.auth.decorators import login_required
# import stripe
# from django.conf import settings
# from django.shortcuts import render, redirect
# from django.contrib import messages

# @login_required
# def transactions(request):
#     transactions = Transaction.objects.filter(user=request.user.profile)
#     return render(request, 'payments/transactions.html', {'transactions': transactions})





# stripe.api_key = settings.STRIPE_SECRET_KEY
# @login_required
# def earnings(request):

    


#     user = request.user

#     # Create a Stripe Express account for the user
#     account = stripe.Account.create(
#         type="express",
#         email="l.ilym.a.nde.rs.on81.3@gmail.com",
#         capabilities={
#         "transfers": {"requested": True}  # Enable Transfers Capability
#     }
#     )

#     # Store the account ID in the user's profile
#     user.profile.stripe_account_id = account.id
#     user.profile.save()
#     account = stripe.Account.retrieve(user.profile.stripe_account_id)
#     if account.capabilities.get("transfers") == "active":
#         print("Transfers are enabled ✅")
#     else:
#         print("Transfers are NOT enabled ❌, please complete onboarding.")

#     # Generate an account link for onboarding
#     account_link = stripe.AccountLink.create(
#         account=account.id,
#         refresh_url="https://yourwebsite.com/stripe/refresh/",
#         return_url="https://yourwebsite.com/dashboard/",
#         type="account_onboarding",
#     )


#     if request.method == "POST":
#         amount = float(request.POST.get("amount"))
#         user = request.user

#         # Check if user has enough balance
#         if user.profile.total_earnings >= amount:
#             if not user.profile.stripe_account_id:  
#                 # If user has no Stripe account ID, show a message
#                 Notification.objects.create(user=user, message="Withdrawal failed: No Stripe account connected.")
#                 messages.error(request, "You need to connect a Stripe account before withdrawing funds.")
#                 return redirect("withdrawal_page")

#             try:
#                 # Transfer money to user's Stripe account
#                 transfer = stripe.Transfer.create(
#                     amount=int(amount * 100),  # Convert to cents
#                     currency="usd",
#                     destination=user.profile.stripe_account_id,
#                     # destination="hello",
#                     description="Withdrawal Request"
#                 )

#                 # Deduct amount from user's total_earnings
#                 user.profile.total_earnings -= amount
#                 user.profile.save()

#                 # Save withdrawal record
#                 Withdrawal.objects.create(user=user, amount=amount, status="Completed")

#                 # Save success notification
#                 Notification.objects.create(user=user, message=f"Your withdrawal of ${amount} was successful.")

#                 messages.success(request, "Withdrawal successful!")
#             except stripe.error.StripeError as e:
#                 Notification.objects.create(user=user, message="Withdrawal failed due to payment gateway error.")
#                 messages.error(request, f"Error: {e.user_message}")
#         else:
#             Notification.objects.create(user=user, message="Withdrawal failed due to insufficient balance.")
#             messages.error(request, "Insufficient funds for withdrawal.")

#         return redirect("home")

#     return render(request, "payments/earnings.html")

# # @login_required
# # def earnings(request):
# #     user = request.user
# #     earnings = Earnings.objects.filter(user=user)
# #     withdrawals = WithdrawalRequest.objects.filter(user=user)

# #     if request.method == "POST":
# #         amount = request.POST.get("amount")
# #         method = request.POST.get("method")
# #         if float(amount) > 0:
# #             WithdrawalRequest.objects.create(user=user, amount=amount, method=method, status="Pending")
    
# #     return render(request, "payments/earnings.html", {"earnings": earnings, "withdrawals": withdrawals})
