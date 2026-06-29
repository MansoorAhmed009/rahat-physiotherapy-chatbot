import os
import smtplib
import logging
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Email config
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
DR_EMAIL_TO = os.getenv("DR_EMAIL_TO", "rahatphysio9@gmail.com")

# Twilio config
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
DR_WHATSAPP_TO = os.getenv("DR_WHATSAPP_TO")

# --- Email ---

def send_email(subject: str, body: str) -> bool:
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.info("Email not configured — notification skipped")
        return False
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = DR_EMAIL_TO

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Email sent to %s", DR_EMAIL_TO)
        return True
    except Exception as e:
        logger.error("Email send failed: %s", e)
        return False


# --- WhatsApp ---

client = None


def get_twilio_client():
    global client
    if client is None and all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN]):
        try:
            from twilio.rest import Client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        except Exception as e:
            logger.warning("Failed to init Twilio client: %s", e)
    return client


def send_whatsapp(message_body: str) -> bool:
    twilio = get_twilio_client()
    if not twilio or not TWILIO_WHATSAPP_FROM or not DR_WHATSAPP_TO:
        logger.info("WhatsApp not configured — notification skipped")
        return False
    try:
        twilio.messages.create(
            body=message_body,
            from_=f"whatsapp:{TWILIO_WHATSAPP_FROM}",
            to=f"whatsapp:{DR_WHATSAPP_TO}",
        )
        logger.info("WhatsApp sent to %s", DR_WHATSAPP_TO)
        return True
    except Exception as e:
        logger.error("WhatsApp send failed: %s", e)
        return False


# --- Notifications ---

def notify_new_appointment(name: str, email: str, phone: str, date: str, time: str):
    subject = f"New Appointment - {name}"
    body = (
        f"New Appointment Booking\n\n"
        f"Patient: {name}\n"
        f"Phone: {phone}\n"
        f"Email: {email}\n"
        f"Date: {date}\n"
        f"Time: {time}\n\n"
        f"Please check your clinic schedule and confirm."
    )
    send_email(subject, body)
    send_whatsapp(body)


def notify_new_lead(name: str, email: str, phone: str, interest: str):
    subject = f"New Inquiry - {name}"
    body = (
        f"New Patient Inquiry\n\n"
        f"Name: {name}\n"
        f"Phone: {phone}\n"
        f"Email: {email}\n"
        f"Interested in: {interest}\n\n"
        f"Please follow up with this patient."
    )
    send_email(subject, body)
    send_whatsapp(body)
