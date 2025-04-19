# payments/views.py

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .paypal import create_order
import requests
from django.conf import settings
from .paypal import get_access_token
from .paypal_config import PayPalClient
from django.shortcuts import render
from django.http import HttpResponse
from .forms import WithdrawalForm
from .models import Withdrawal
from users.models import Profile  # Update if stored elsewhere
from payments.models import CreatorEarnings
from django.contrib import messages
from payments.models import CreatorEarnings, Withdrawal

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CreatorEarnings, Withdrawal
from .paypal_client import paypalrestsdk

@login_required
def request_withdrawal(request):
    earnings, created = CreatorEarnings.objects.get_or_create(user=request.user)
    # user_email = request.user.profile.paypal_email  # <-- must exist
    # user_email = request.user.email  # <-- must exist
    # user_email = "sb-6vuue40001621@personal.example.com"  # <-- must exist

    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            user_email = request.POST.get('email')
        except (TypeError, ValueError):
            messages.error(request, "Invalid amount.")
            return redirect('request_withdrawal')

        if earnings.available_balance >= 10 and amount <= earnings.available_balance:
            # 🟡 Send payout via PayPal
            payout = paypalrestsdk.Payout({
                "sender_batch_header": {
                    "sender_batch_id": str(request.user.id) + str(amount),
                    "email_subject": "You have a payout from EchoesRipple!"
                },
                "items": [{
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": str(amount),
                        "currency": "USD"
                    },
                    "receiver": user_email,
                    "note": "Thanks for using EchoesRipple!",
                    "sender_item_id": "item_1"
                }]
            })

            if payout.create():
                # Save record locally
                Withdrawal.objects.create(user=request.user, amount=amount, status="Paid")
                earnings.available_balance -= amount
                earnings.save()
                messages.success(request, f"Payout of ${amount} sent to your PayPal.")
                return redirect('withdrawal_success')
            else:
                print(payout.error)
                messages.error(request, "PayPal payout failed. Please try again.")
                return redirect('request_withdrawal')
        else:
            messages.error(request, "Minimum withdrawal is $10 or insufficient balance.")
            return redirect('request_withdrawal')

    return render(request, 'payments/request_withdrawal.html', {'earnings': earnings})

# @login_required
# def request_withdrawal(request):
#     earnings, created = CreatorEarnings.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         try:
#             amount = float(request.POST.get('amount'))
#         except (TypeError, ValueError):
#             messages.error(request, "Invalid amount.")
#             return redirect('request_withdrawal')

#         if earnings.available_balance >= 10 and amount <= earnings.available_balance:
#             Withdrawal.objects.create(user=request.user, amount=amount)
#             earnings.available_balance -= amount
#             earnings.save()
#             messages.success(request, "Withdrawal request submitted.")
#             return redirect('withdrawal_success')
#         else:
#             messages.error(request, "Minimum withdrawal is $10 or insufficient balance.")
            
#         return redirect('request_withdrawal')

#     return render(request, 'payments/request_withdrawal.html', {'earnings': earnings})

def add_view(content, viewer):
    creator = content.uploaded_by.user
    earning = 0.01  # example: $0.01 per view
    content.earnings += earning
    content.save()

    ce, created = CreatorEarnings.objects.get_or_create(user=creator)
    ce.total_earned += earning
    ce.available_balance += earning
    ce.save()

# @login_required
# def request_withdrawal(request):
#     profile = request.user.profile

#     if request.method == 'POST':
#         form = WithdrawalForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             if amount <= profile.balance:
#                 Withdrawal.objects.create(user=request.user, amount=amount)
#                 profile.withdrawn_amount += amount
#                 profile.save()
#                 return redirect('withdrawal_success')  # Add this page
#             else:
#                 form.add_error('amount', 'Insufficient balance')
#     else:
#         form = WithdrawalForm()

#     return render(request, 'payments/request_withdrawal.html', {'form': form, 'balance': profile.balance})

def paypal_success(request):
    order_id = request.GET.get('token')  # PayPal sends ?token=ORDER_ID in return URL
    if not order_id:
        return HttpResponse("Order ID not found.", status=400)

    client = PayPalClient()
    response = client.post(f"/v2/checkout/orders/{order_id}/capture", json={})
    capture_data = response.json()

    # Optional: Save capture_data to database for record
    # You can extract payment details like amount, payer email, etc.
    amount = capture_data['purchase_units'][0]['payments']['captures'][0]['amount']['value']
    currency = capture_data['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
    payer_email = capture_data['payer']['email_address']

    context = {
        "amount": amount,
        "currency": currency,
        "payer_email": payer_email,
        "capture_data": capture_data
    }

    return render(request, 'payments/success.html', context)



def create_paypal_order(request):
    client = PayPalClient()
    body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "2.99"
                }
            }
        ],
        "application_context": {
            "return_url": "http://localhost:8000/payments/success/",
            "cancel_url": "http://localhost:8000/payments/cancel/"
        }
    }

    response = client.post("/v2/checkout/orders", json=body)
    data = response.json()

    for link in data["links"]:
        if link["rel"] == "approve":
            return JsonResponse({"redirect_url": link["href"]})

def start_payment(request, amount):
    order = create_order(amount = float(amount))  # Set your amount dynamically
    for link in order['links']:
        if link['rel'] == 'approve':
            return redirect(link['href'])
    return render(request, 'payments/error.html', {'error': 'Could not initiate payment.'})


def complete_payment(request):
    token = request.GET.get('token')
    if not token:
        return render(request, 'payments/error.html', {'message': 'Token is missing.'})

    url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{token}/capture"
    access_token = get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(url, headers=headers)
    payment_result = response.json()

    if response.status_code != 201:
        return render(request, 'payments/error.html', {'message': payment_result})

    # Optionally save to DB, update user's purchase history, etc.
    return render(request, 'payments/success.html', {'payment': payment_result})


def withdrawal_success(request):
    return render(request, 'payments/withdrawal_success.html')