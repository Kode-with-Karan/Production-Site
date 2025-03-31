from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings

def send_email(subject, message, recipient_list, use_secondary=False):
    """Send email using primary or secondary email configuration"""
    
    if use_secondary:
        backend = EmailBackend(
            host=settings.SECONDARY_EMAIL_CONFIG["EMAIL_HOST"],
            port=settings.SECONDARY_EMAIL_CONFIG["EMAIL_PORT"],
            username=settings.SECONDARY_EMAIL_CONFIG["EMAIL_HOST_USER"],
            password=settings.SECONDARY_EMAIL_CONFIG["EMAIL_HOST_PASSWORD"],
            use_tls=settings.SECONDARY_EMAIL_CONFIG["EMAIL_USE_TLS"],
        )
        from_email = settings.SECONDARY_EMAIL_CONFIG["EMAIL_HOST_USER"]
    else:
        backend = None  # Use default Django email backend
        from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        connection=backend,
    )
