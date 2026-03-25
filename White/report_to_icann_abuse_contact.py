import requests
import tldextract
import smtplib
from email.message import EmailMessage

# === Config ===
SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"
ORG_NAME = "Black Ops | ISF"

def extract_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def get_icann_abuse_contact(domain):
    try:
        url = f"https://rdap.org/domain/{domain}"
        response = requests.get(url)
        data = response.json()

        # Look for abuse contact
        for entity in data.get("entities", []):
            roles = entity.get("roles", [])
            if "abuse" in roles:
                for vcard in entity.get("vcardArray", [[], []])[1]:
                    if vcard[0] == "email":
                        abuse_email = vcard[3]
                        return abuse_email
        return None
    except Exception as e:
        print(f"[!] Failed to fetch ICANN abuse contact: {e}")
        return None

def send_email(to_email, domain, url):
    msg = EmailMessage()
    msg["Subject"] = f"Phishing Domain Report - {domain}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg.set_content(f"""Dear Registrar Abuse Team,

This is to notify you of a phishing website registered under your service:

URL: {url}
Domain: {domain}

This site is actively stealing credentials and impersonating a legitimate service. Please investigate in accordance with your ICANN obligations.

Thank you,
{ORG_NAME}
Contact: {SENDER_EMAIL}
""")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[✓] Abuse report sent to: {to_email}")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

def report_to_icann_abuse_contact(url):
    domain = extract_domain(url)
    abuse_email = get_icann_abuse_contact(domain)
    if abuse_email:
        send_email(abuse_email, domain, url)
        return f"[✓] Abuse report sent to: {abuse_email}"
    else:
        # Optionally, send to ICANN's default compliance address
        return "[!] Abuse contact not found. Consider reporting to: compliance@icann.org"
