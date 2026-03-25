import socket
import smtplib
import tldextract
import whois
from email.message import EmailMessage

# === Config ===
SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use Gmail App Password
ORG_NAME = "Black Ops | ISF"

# === Step 1: Extract domain
def extract_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

# === Step 2: Get IP address from domain
def get_ip_from_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception as e:
        print(f"[!] Could not resolve IP: {e}")
        return None

# === Step 3: WHOIS lookup for abuse email
def get_abuse_email(domain):
    try:
        w = whois.whois(domain)
        if isinstance(w.emails, list):
            abuse_emails = [email for email in w.emails if "abuse" in email.lower()]
        elif isinstance(w.emails, str) and "abuse" in w.emails.lower():
            abuse_emails = [w.emails]
        else:
            abuse_emails = []
        return abuse_emails
    except Exception as e:
        print(f"[!] WHOIS lookup failed: {e}")
        return []

# === Step 4: Send abuse email
def send_to_isp(abuse_email, url, hosting_domain):
    msg = EmailMessage()
    msg['Subject'] = f"Phishing Website Abuse Report - {hosting_domain}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = abuse_email

    msg.set_content(f"""Dear Hosting Provider,

We have detected a phishing site hosted under your infrastructure:

{url}

This site is impersonating legitimate services and collecting user credentials fraudulently.

Please take action per your abuse policies to investigate and remove the malicious content.

Sincerely,
{ORG_NAME}
Contact: {SENDER_EMAIL}
""")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[✓] Report sent to ISP abuse contact: {abuse_email}")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

# === Main Execution
def report_to_isp(url):
    domain = extract_domain(url)
    print(f"[*] Extracted domain: {domain}")

    ip = get_ip_from_domain(domain)
    print(f"[*] Resolved IP: {ip}")

    abuse_emails = get_abuse_email(domain)
    if abuse_emails:
        for abuse_email in abuse_emails:
            send_to_isp(abuse_email, url, domain)
        return f"[✓] Report sent to ISP abuse contact(s): {', '.join(abuse_emails)}"
    else:
        print("[!] No abuse email found for hosting ISP. WHOIS may be protected or missing data.")
        return "[!] No abuse email found for hosting ISP. WHOIS may be protected or missing data."