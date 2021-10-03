from django.conf import settings
from email_tools.emails import send_email
from sentry_sdk import capture_message
from twilio.base.exceptions import TwilioException, TwilioRestException
from twilio.rest import Client


def sendSMSVerification(to, verification_code):
    try:
        client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
        body = f"Your Penn Labs Account Verification Code is: {verification_code}"
        client.messages.create(to=str(to), from_=settings.TWILIO_NUMBER, body=body)
    except TwilioRestException as e:
        capture_message(e, level="error")
    except TwilioException as e:  # likely a credential issue in development
        capture_message(e, level="error")


def sendEmailVerification(to, verification_code):
    context = {
        "verification_code": verification_code,
    }
    subject = "Penn Labs email verification"
    send_email("emails/email_verification.html", context, subject, to)
