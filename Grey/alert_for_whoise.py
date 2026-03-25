import whois
import smtplib
import time
import sys
import os
from email.message import EmailMessage
from datetime import datetime
import tldextract

# === CONFIGURATION ===
CHECK_INTERVAL = 3600  # Time between checks in seconds (3600s = 1 hour)
STORAGE_FILE = "whois_last.txt"

# === Email Settings ===
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "recipient_email@gmail.com"
SMTP_USERNAME = EMAIL_FROM
SMTP_PASSWORD = "your_gmail_app_password"  # Use Gmail App Password

# === WHOIS Fetcher ===
def extract_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def fetch_whois(domain):
    try:
        w = whois.whois(domain)
        return str(w)
    except Exception as e:
        print(f"[!] Error fetching WHOIS for {domain}: {e}")
        return None

# === Load Previously Stored WHOIS ===
def load_last_whois():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return f.read()
    return None

# === Save WHOIS Snapshot ===
def save_whois(data):
    with open(STORAGE_FILE, "w") as f:
        f.write(data)

# === Send Email Alert ===
def send_email(subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print("[✓] Alert email sent.")
    except Exception as e:
        print(f"[X] Failed to send alert: {e}")

# === Main Monitoring Loop ===
def main(url):
    domain = extract_domain(url)
    print(f"[•] WHOIS Monitor started for domain: {domain}")
    while True:
        current_whois = fetch_whois(domain)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not current_whois:
            print(f"[!] Skipping this check due to fetch error at {now}")
        else:
            last_whois = load_last_whois()
            if last_whois is None:
                print(f"[+] First-time run. Saving WHOIS snapshot at {now}")
                save_whois(current_whois)
                send_email(
                    f"[Init] WHOIS monitoring started for {domain}",
                    f"Monitoring started for {domain} at {now}.\n\nInitial WHOIS:\n{current_whois}"
                )
            elif current_whois != last_whois:
                print(f"[⚠] WHOIS changed for {domain} at {now}")
                save_whois(current_whois)
                send_email(
                    f"[Change] WHOIS updated for {domain}",
                    f"WHOIS for {domain} changed at {now}.\n\nNew WHOIS data:\n{current_whois}"
                )
            else:
                print(f"[✓] No change at {now}")

        time.sleep(CHECK_INTERVAL)

# === For GUI/External Use ===
def run_whois_monitor(url):
    """
    Starts the WHOIS monitoring loop in a background thread for GUI use.
    """
    import threading
    def monitor():
        try:
            main(url)
        except Exception as e:
            print(f"[!] WHOIS monitor error: {e}")
    threading.Thread(target=monitor, daemon=True).start()

