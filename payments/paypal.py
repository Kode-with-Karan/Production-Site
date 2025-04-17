# payments/paypal.py
import requests
from django.conf import settings


def get_access_token():
    print(settings.PAYPAL_API_BASE)
    url = f"{settings.PAYPAL_API_BASE}/v1/oauth2/token"
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(url, headers=headers, data=data, auth=auth)
    return response.json().get('access_token')


def create_order(amount, currency='USD'):
    access_token = get_access_token()
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": currency,
                "value": str(amount)
            }
        }],
        "application_context": {
            "return_url": "http://localhost:8000/payments/complete/",
            "cancel_url": "http://localhost:8000/payments/cancel/"
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()