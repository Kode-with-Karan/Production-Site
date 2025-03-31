import stripe

stripe.api_key = "your_stripe_secret_key"

def process_payment(user, amount):
    # try:
    #     # Simulate a successful payment (Replace with actual Stripe/Adyen integration)
    #     charge = stripe.Charge.create(
    #         amount=int(amount * 100),  # Convert to cents
    #         currency="usd",
    #         description=f"Promotion Payment by {user.username}",
    #         source="tok_visa",  # Test card
    #     )
    #     return charge["paid"]  # Returns True if payment is successful
    # except stripe.error.StripeError:
    #     return False
    return True