import webbrowser
import smtplib
from email.message import EmailMessage

# === Config ===
SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"
ORG_NAME = "Black Ops | ISF"

def report_to_mozilla_form(url):
    print("[*] Opening Google Safe Browsing form (used by Firefox)...")
    webbrowser.open(f"https://safebrowsing.google.com/safebrowsing/report_phish/?url={url}")
    print("[✓] Please complete the CAPTCHA to submit.")

def report_to_mozilla_email(url):
    print("[*] Sending optional report email to Mozilla...")
    msg = EmailMessage()
    msg["Subject"] = "Phishing Site Report - Firefox User"
    msg["From"] = SENDER_EMAIL
    msg["To"] = "abuse@mozilla.org"

    msg.set_content(f"""
Dear Mozilla Security Team,

I would like to report a phishing site encountered via the Firefox browser.

Phishing URL: {url}

It appears to be impersonating legitimate services to harvest credentials.

Thank you,
{ORG_NAME}
Contact: {SENDER_EMAIL}
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print("[✓] Email sent to abuse@mozilla.org")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

# ===Main Function===
def report_to_mozilla(url):
    report_to_mozilla_form(url)
    report_to_mozilla_email(url)
    return "[✓] Mozilla Safe Browsing form opened and optional email sent."
