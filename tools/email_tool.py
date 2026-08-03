import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

def send_vendor_email(
    to_email: str,
    subject: str,
    body: str,
    is_html: bool = False,
    sender_email: Optional[str] = None,
    sender_password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sends an email using standard free Gmail SMTP (smtp.gmail.com:587) with STARTTLS.
    No paid third-party platforms (like SendGrid or Resend) required.
    
    Requires a Google App Password (not your standard login password) if using Gmail.
    
    Args:
        to_email: Recipient email address.
        subject: Email subject line.
        body: Plain text or HTML email body.
        is_html: True if body contains HTML formatting.
        sender_email: Sender Gmail address (defaults to SENDER_EMAIL or GMAIL_ADDRESS env var).
        sender_password: Gmail App Password (defaults to SENDER_PASSWORD or GMAIL_APP_PASSWORD env var).
        
    Returns:
        Dict containing success status, message, and error details if any.
    """
    # Load credentials from parameters or environment variables
    from_addr = sender_email or os.getenv("SENDER_EMAIL") or os.getenv("GMAIL_ADDRESS")
    app_pwd = sender_password or os.getenv("SENDER_PASSWORD") or os.getenv("GMAIL_APP_PASSWORD")

    # Dry-run fallback mode if credentials are missing
    if not from_addr or not app_pwd or app_pwd.startswith("your-app-password"):
        print(f"⚠️ [SMTP DRY-RUN MODE]: Credentials not configured. Simulating email dispatch to '{to_email}'.")
        return {
            "success": True,
            "dry_run": True,
            "message": f"[DRY-RUN] Email to {to_email} simulated successfully.",
            "details": {
                "to": to_email,
                "subject": subject,
                "body_preview": body[:200] + "..." if len(body) > 200 else body
            },
            "error": None
        }

    try:
        # Create MIME message container
        msg = MIMEMultipart("alternative")
        msg["From"] = from_addr
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach text or HTML body
        mime_type = "html" if is_html else "plain"
        msg.attach(MIMEText(body, mime_type, "utf-8"))

        # Connect to Gmail SMTP server
        with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()  # Secure connection with TLS
            server.ehlo()
            server.login(from_addr, app_pwd)
            server.sendmail(from_addr, [to_email], msg.as_string())

        return {
            "success": True,
            "dry_run": False,
            "message": f"Email successfully sent to {to_email} via Gmail SMTP.",
            "details": {
                "to": to_email,
                "subject": subject
            },
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "dry_run": False,
            "message": f"Failed to send email to {to_email} via Gmail SMTP.",
            "details": None,
            "error": str(e)
        }


# Quick CLI test block
if __name__ == "__main__":
    print("📧 Testing VendorMind Free Gmail SMTP Email Tool...")
    test_res = send_vendor_email(
        to_email="vendor-sales@example.com",
        subject="VendorMind RFQ & Negotiation Proposal",
        body="Dear Vendor Sales Team,\n\nWe are submitting our counter-offer regarding the enterprise quote..."
    )
    print("Result:", test_res)
