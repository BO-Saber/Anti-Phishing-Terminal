import smtplib
import tldextract
import whois
from email.message import EmailMessage

# === Config ===
SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Gmail App Password
ORG_NAME = "Black Ops | ISF"

# === Step 1: Extract domain from URL
def extract_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

# === Step 2: WHOIS lookup to get registrar and abuse contact
def get_registrar_abuse_email(domain):
    try:
        w = whois.whois(domain)
        registrar_name = w.registrar or "Unknown Registrar"
        abuse_emails = []

        if hasattr(w, 'emails'):
            if isinstance(w.emails, list):
                abuse_emails = [e for e in w.emails if "abuse" in e.lower()]
            elif isinstance(w.emails, str) and "abuse" in w.emails.lower():
                abuse_emails = [w.emails]

        return registrar_name, abuse_emails
    except Exception as e:
        print(f"[!] WHOIS lookup failed: {e}")
        return "Unknown", []

# === Step 3: Send report email
def send_to_registrar(registrar_name, abuse_email, url, domain):
    msg = EmailMessage()
    msg['Subject'] = f"Phishing Abuse Report - {domain}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = abuse_email

    msg.set_content(f"""Dear {registrar_name} Abuse Team,

We have identified a phishing domain registered under your service:

URL: {url}
Domain: {domain}

This domain is actively involved in phishing attacks and is impersonating legitimate services to steal user credentials.

Please take appropriate action per your registrar policies and ICANN rules.

Sincerely,
{ORG_NAME}
Contact: {SENDER_EMAIL}
""")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[✓] Report sent to registrar: {abuse_email}")
    except Exception as e:
        print(f"[!] Failed to send abuse report: {e}")

# === Main Logic
def report_to_registrar(url):
    domain = extract_domain(url)
    registrar, abuse_contacts = get_registrar_abuse_email(domain)
    if abuse_contacts:
        for abuse_email in abuse_contacts:
            send_to_registrar(registrar, abuse_email, url, domain)
        return f"[✓] Report sent to registrar abuse contact(s): {', '.join(abuse_contacts)}"
    else:
        return "[!] No abuse email found for registrar. WHOIS may be protected."
