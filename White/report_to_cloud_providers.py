import socket
import smtplib
import tldextract
import whois
import webbrowser
from email.message import EmailMessage

SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"
ORG_NAME = "Black Ops | ISF"

# Known cloud providers and how to report to them
CLOUD_PROVIDERS = [
    {"name": "Amazon AWS", "match": "amazonaws.com", "method": "form", "contact": "https://aws.amazon.com/forms/report-abuse"},
    {"name": "Microsoft Azure", "match": "azure", "method": "form", "contact": "https://www.microsoft.com/en-us/wdsi/support/report-unsafe-site"},
    {"name": "Google Cloud", "match": "google", "method": "form", "contact": "https://support.google.com/legal/troubleshooter/1114905"},
    {"name": "Cloudflare", "match": "cloudflare", "method": "form", "contact": "https://abuse.cloudflare.com/"},
    {"name": "DigitalOcean", "match": "digitalocean", "method": "email", "contact": "abuse@digitalocean.com"},
    {"name": "Linode", "match": "linode", "method": "email", "contact": "abuse@linode.com"},
    {"name": "Hetzner", "match": "hetzner", "method": "form", "contact": "https://abuse.hetzner.com/"},
    {"name": "OVH", "match": "ovh", "method": "form", "contact": "https://www.ovh.com/abuse/"}
]

# Extract the domain from the URL
def extract_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

# Get IP of the domain
def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception as e:
        print(f"[!] Failed to get IP: {e}")
        return None

# Perform WHOIS and match to known providers
def get_cloud_provider(domain):
    try:
        w = whois.whois(domain)
        host_info = str(w).lower()
        for provider in CLOUD_PROVIDERS:
            if provider["match"] in host_info:
                return provider
        return None
    except Exception as e:
        print(f"[!] WHOIS failed: {e}")
        return None

# Send email if provider method is email
def send_abuse_email(to_email, url, provider_name):
    msg = EmailMessage()
    msg['Subject'] = f"Phishing Abuse Report - Hosted on {provider_name}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg.set_content(f"""Dear {provider_name} Abuse Team,

We have detected phishing activity hosted under your infrastructure.

Phishing URL: {url}

Please investigate and take appropriate action as per your abuse policy.

Sincerely,
{ORG_NAME}
Email: {SENDER_EMAIL}
""")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[✓] Report sent to {provider_name} via email.")
    except Exception as e:
        print(f"[!] Failed to send email to {provider_name}: {e}")

# Main logic
def report_to_cloud_providers(url):
    domain = extract_domain(url)
    ip = get_ip(domain)
    print(f"[*] Domain: {domain}, IP: {ip}")

    provider = get_cloud_provider(domain)
    if provider:
        print(f"[✓] Hosting Cloud Provider Detected: {provider['name']}")
        if provider["method"] == "form":
            print(f"[*] Opening report form for {provider['name']}")
            webbrowser.open(provider["contact"])
            return f"[✓] Opened report form for {provider['name']}."
        elif provider["method"] == "email":
            send_abuse_email(provider["contact"], url, provider["name"])
            return f"[✓] Abuse email sent to {provider['name']}."
    else:
        print("[!] No known cloud provider detected via WHOIS. Try checking IP manually via ipinfo.io or abuseipdb.com.")
        return "[!] No known cloud provider detected via WHOIS."