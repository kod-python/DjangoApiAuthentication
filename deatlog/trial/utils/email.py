from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

def generate_reset_token():
    return get_random_string(length=32)

def send_reset_email(email: str, token: str):
    subject = "Password Reset Request"
    # reset_link = f"{settings.RESET_URL}?token={token}"
    reset_link = f"token={token}"
    message = f"Click the link below to reset your password:\n\n{reset_link}"
    email_message = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
    email_message.send()

def save_reset_token(user, token):
    # Save the token and its expiry time
    user.reset_token = token
    user.reset_token_expiry = timezone.now() + timedelta(hours=1)  # Token valid for 1 hour
    user.save()

def verify_token(user, token):
    return user.reset_token == token and user.reset_token_expiry > timezone.now()











# from django.core.mail import EmailMessage
# from django.conf import settings

# def send_reset_email(email: str, token: str):
#     subject = "Password Reset Request"
#     reset_link = f"{settings.RESET_URL}?token={token}"
#     message = f"Click the link below to reset your password:\n\n{reset_link}"
#     email_message = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
#     email_message.send()










# from django.core.mail import EmailMessage
# from django.conf import settings

# def send_reset_email(email: str, token: str):
#     subject = "Password Reset Request"
#     message = f"Click the link below to reset your password:\n\n{settings.RESET_URL}?token={token}"
#     email_message = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
#     email_message.send()
