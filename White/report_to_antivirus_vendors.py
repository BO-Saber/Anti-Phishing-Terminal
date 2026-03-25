import webbrowser
import smtplib
from email.message import EmailMessage

# === Configuration ===
SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"
ORG_NAME = "Black Ops | ISF"

AV_VENDORS = [
    {"name": "Norton (Symantec)", "method": "form", "contact": "https://submit.norton.com/?type=phish"},
    {"name": "McAfee", "method": "form", "contact": "https://www.mcafee.com/enterprise/en-in/threat-center/report-a-suspected-site.html"},
    {"name": "Kaspersky", "method": "form", "contact": "https://opentip.kaspersky.com"},
    {"name": "Avast", "method": "form", "contact": "https://www.avast.com/report-phishing"},
    {"name": "Bitdefender", "method": "email", "contact": "phishing@bitdefender.com"},
    {"name": "ESET", "method": "email", "contact": "samples@eset.com"},
    {"name": "Trend Micro", "method": "form", "contact": "https://global.sitesafety.trendmicro.com/"},
    {"name": "F-Secure", "method": "email", "contact": "samples@f-secure.com"},
    {"name": "Malwarebytes", "method": "form", "contact": "https://www.malwarebytes.com/report"},
]

def send_email(to_email, subject, content):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg.set_content(content)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[✓] Report sent to: {to_email}")
    except Exception as e:
        print(f"[!] Failed to send email to {to_email}: {e}")

def report_to_av_vendors(url):
    print(f"[*] Starting report for phishing URL: {url}")
    for vendor in AV_VENDORS:
        if vendor["method"] == "form":
            print(f"[*] Opening report form for {vendor['name']}")
            webbrowser.open(vendor["contact"])
        elif vendor["method"] == "email":
            print(f"[*] Sending email report to {vendor['name']}")
            subject = f"Phishing URL Report - {url}"
            content = f"""Dear {vendor['name']} Security Team,

This is to report a phishing website:

{url}

Please investigate and block it according to your threat policy.

Regards,
{ORG_NAME}
Contact: {SENDER_EMAIL}
"""
            send_email(vendor["contact"], subject, content)

