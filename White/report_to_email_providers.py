import smtplib
import re
import requests
from email.message import EmailMessage

# === Config ===
SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use Gmail App Password
ORG_NAME = "Black Ops | ISF"

EMAIL_PROVIDERS = [
    {"name": "Gmail", "domain": "gmail.com", "contact": "abuse@gmail.com"},
    {"name": "Yahoo", "domain": "yahoo.com", "contact": "abuse@yahoo.com"},
    {"name": "Outlook", "domain": "outlook.com", "contact": "abuse@outlook.com"},
    {"name": "Hotmail", "domain": "hotmail.com", "contact": "abuse@hotmail.com"},
    {"name": "ProtonMail", "domain": "protonmail.com", "contact": "abuse@protonmail.ch"},
    {"name": "Zoho", "domain": "zoho.com", "contact": "abuse@zohocorp.com"},
    {"name": "AOL", "domain": "aol.com", "contact": "abuse@aol.com"},
    {"name": "iCloud", "domain": "icloud.com", "contact": "abuse@apple.com"},
    {"name": "Yandex", "domain": "yandex.com", "contact": "abuse@yandex.ru"},
    {"name": "Mail.ru", "domain": "mail.ru", "contact": "abuse@mail.ru"},
    {"name": "GMX", "domain": "gmx.com", "contact": "abuse@gmx.com"}
]

# === Step 1: Extract emails from the phishing site ===
def extract_emails_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[!] Failed to fetch website: HTTP {response.status_code}")
            return []

        # Basic regex for email detection
        email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        emails = re.findall(email_regex, response.text)
        return list(set(emails))  # Deduplicate
    except Exception as e:
        print(f"[!] Error fetching URL: {e}")
        return []

# === Step 2: Send to provider ===
def send_alert(provider_name, abuse_email, url, attacker_email):
    msg = EmailMessage()
    msg['Subject'] = "Phishing Website Alert – Malicious Email Usage"
    msg['From'] = SENDER_EMAIL
    msg['To'] = abuse_email

    msg.set_content(f"""Dear {provider_name} Abuse Team,

We have identified a phishing campaign involving the website:
{url}

The attacker appears to be using or spoofing the email:
{attacker_email}

This email is being used in phishing activity. Please take appropriate action per your abuse policy.

Sincerely,
{ORG_NAME}
Email: {SENDER_EMAIL}
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[+] Report sent to {provider_name}")
    except Exception as e:
        print(f"[!] Failed to report to {provider_name}: {e}")

# === Step 3: Run ===
def report_to_email_providers(url):
    print(f"[*] Extracting emails from {url}")
    found_emails = extract_emails_from_url(url)

    if found_emails:
        print(f"[+] Found emails: {found_emails}")
        suspicious_email = found_emails[0]
    else:
        # In GUI, you may want to prompt the user instead of input()
        suspicious_email = None

    if not suspicious_email:
        print("[X] No email provided. Exiting.")
        return

    for provider in EMAIL_PROVIDERS:
        if provider["domain"] in suspicious_email.lower():
            send_alert(provider["name"], provider["contact"], url, suspicious_email)
