"""
Email Service: Handle sending notifications via SMTP.
"""
import smtplib
from email.message import EmailMessage
import os
from app.utils.logger import logger

def send_notification_email(email_to: str, subject: str, content: str) -> None:
    """Send an email notification via SMTP in the background."""
    smtp_host = os.getenv("SMTP_HOST", "smtp.example.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "noreply@healthlens.ai")
    smtp_pass = os.getenv("SMTP_PASSWORD", "mockpassword")
    
    # Check if SMTP is enabled in config, for local dev you might want to skip or mock
    if os.getenv("MOCK_SMTP", "true").lower() == "true":
        logger.info(f"[MOCK SMTP] Sending email to {email_to} | Subject: {subject} | Content: {content}")
        return

    try:
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = email_to

        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls()
            if smtp_pass:
                smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        logger.info(f"Email sent successfully to {email_to}")
    except Exception as e:
        logger.error(f"Failed to send email to {email_to}: {str(e)}")
