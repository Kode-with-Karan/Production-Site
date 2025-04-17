import json
from paypalhttp import HttpClient, Environment

class PayPalEnvironment(Environment):
    def __init__(self, client_id, client_secret):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api-m.sandbox.paypal.com"  # use live link for production

    def authorization(self):
        return self.client_id, self.client_secret

class PayPalClient(HttpClient):
    def __init__(self):
        self.client_id = "YOUR_CLIENT_ID"
        self.client_secret = "YOUR_CLIENT_SECRET"
        environment = PayPalEnvironment(self.client_id, self.client_secret)
        super().__init__(environment)
