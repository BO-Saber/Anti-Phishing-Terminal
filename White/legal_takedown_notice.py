import smtplib
import whois
import tldextract
from email.message import EmailMessage
sender_email = "official.blackops.isf@gmail.com"
sender_password = "#Blackops3.0-isf"

def extract_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def get_abuse_email(domain):
    try:
        w = whois.whois(domain)
        emails = w.emails
        if isinstance(emails, list):
            abuse_emails = [e for e in emails if "abuse" in e.lower()]
        elif isinstance(emails, str):
            abuse_emails = [emails] if "abuse" in emails.lower() else []
        return abuse_emails if abuse_emails else None
    except Exception as e:
        return None
    

def legal_takedown_notice(url, sender_email, sender_password, org_name="Black Ops, ISF", manual_email=None):
    domain = extract_domain(url)
    abuse_emails = get_abuse_email(domain)
    if not abuse_emails and manual_email:
        abuse_emails = [manual_email]
    if not abuse_emails:
        return None 
    msg = EmailMessage()
    msg['Subject'] = f"URGENT: Takedown Request for Phishing Domain - {domain}"
    msg['From'] = sender_email
    msg['To'] = ", ".join(abuse_emails)
    msg.set_content(f"""Dear Hosting Provider,
We have identified a phishing website hosted on your infrastructure:
{url}
This site is impersonating legitimate services and fraudulently collecting user credentials.
We request immediate investigation and removal of this domain in accordance with your abuse policies.
Sincerely,
{org_name}
""")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return f"[+] Legal notice sent to: {', '.join(abuse_emails)}"
    except Exception as e:
        return f"[!] Failed to send email: {e}"
