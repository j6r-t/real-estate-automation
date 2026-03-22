"""
Email notification service.
Currently logs to console — replace send_email() with real SMTP or n8n webhook later.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@luxeestate.com")

def send_email(to_email: str, subject: str, body_html: str):
    """Send email via SMTP. Falls back to console logging if not configured."""
    if not SMTP_HOST or not SMTP_USER:
        # Console fallback for development
        print(f"\n{'='*50}")
        print(f"📧 EMAIL (not sent — no SMTP configured)")
        print(f"  TO: {to_email}")
        print(f"  SUBJECT: {subject}")
        print(f"  BODY: {body_html[:200]}...")
        print(f"{'='*50}\n")
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
    except Exception as e:
        print(f"❌ Email failed: {e}")


def notify_appointment_confirmed(client_email: str, client_name: str, property_title: str, date_time: str, agent_name: str):
    subject = "✅ Your Appointment is Confirmed – Luxe Estate"
    body = f"""
    <h2>Your Appointment is Confirmed!</h2>
    <p>Dear {client_name},</p>
    <p>Your visit to <strong>{property_title}</strong> has been confirmed.</p>
    <ul>
        <li><strong>Date & Time:</strong> {date_time}</li>
        <li><strong>Agent:</strong> {agent_name}</li>
    </ul>
    <p>If you need to reschedule, please contact us.</p>
    <br><p>Luxe Estate Team</p>
    """
    send_email(client_email, subject, body)


def notify_appointment_cancelled(client_email: str, client_name: str, property_title: str, date_time: str, reason: str = ""):
    subject = "❌ Appointment Cancelled – Luxe Estate"
    body = f"""
    <h2>Appointment Cancellation Notice</h2>
    <p>Dear {client_name},</p>
    <p>We regret to inform you that your appointment for <strong>{property_title}</strong> on <strong>{date_time}</strong> has been cancelled.</p>
    {f'<p><strong>Reason:</strong> {reason}</p>' if reason else ''}
    <p>Please contact us to reschedule.</p>
    <br><p>Luxe Estate Team</p>
    """
    send_email(client_email, subject, body)


def notify_appointment_rescheduled(client_email: str, client_name: str, property_title: str, new_date_time: str):
    subject = "🔄 Appointment Rescheduled – Luxe Estate"
    body = f"""
    <h2>Your Appointment Has Been Rescheduled</h2>
    <p>Dear {client_name},</p>
    <p>Your visit to <strong>{property_title}</strong> has been rescheduled.</p>
    <p><strong>New Date & Time:</strong> {new_date_time}</p>
    <p>If this doesn't work for you, please contact us.</p>
    <br><p>Luxe Estate Team</p>
    """
    send_email(client_email, subject, body)
