# utils/paypal.py
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

def get_paypal_access_token():
    url = f"{settings.PAYPAL_API_BASE}/v1/oauth2/token"
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data,
                             auth=HTTPBasicAuth(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET))
    
    return response.json().get("access_token")


def create_paypal_order(amount):
    access_token = get_paypal_access_token()
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": f"{amount:.2f}"
            }
        }],
        "application_context": {
            "return_url": "http://localhost:8000/payment/success/",
            "cancel_url": "http://localhost:8000/payment/cancel/"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def capture_paypal_payment(order_id):
    access_token = get_paypal_access_token()
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.post(url, headers=headers)
    return response.json()
