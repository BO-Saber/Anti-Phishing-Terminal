import smtplib
import webbrowser
from email.message import EmailMessage

# === Config ===
SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use Gmail App Password
ORG_NAME = "Black Ops | ISF"

# === Built-in CERT contact database ===
CERT_DATABASE = [
    {
        "country": "India",
        "team": "CERT-In",
        "method": "email",
        "contact": "incident@cert-in.org.in"
    },
    {
        "country": "USA",
        "team": "US-CERT",
        "method": "form",
        "contact": "https://www.cisa.gov/report"
    },
    {
        "country": "United Kingdom",
        "team": "NCSC",
        "method": "email",
        "contact": "report@phishing.gov.uk"
    },
    {
        "country": "Japan",
        "team": "JPCERT/CC",
        "method": "form",
        "contact": "https://form.jpcert.or.jp/"
    },
    {
        "country": "Germany",
        "team": "BSI",
        "method": "email",
        "contact": "cert@bsi.bund.de"
    },
    {
        "country": "Australia",
        "team": "ACSC",
        "method": "form",
        "contact": "https://www.cyber.gov.au/report-and-recover/report"
    },
    {
        "country": "Canada",
        "team": "Cyber Centre",
        "method": "form",
        "contact": "https://www.cyber.gc.ca/en/report"
    },
    {
        "country": "France",
        "team": "CERT-FR",
        "method": "email",
        "contact": "cert-fr.cossi@ssi.gouv.fr"
    },
    {
        "country": "Brazil",
        "team": "CERT.br",
        "method": "form",
        "contact": "https://www.cert.br/report"
    }
    # 🔧 Add more CERTs here as needed
]

# === Email Sender Function ===
def send_email(team, country, recipient_email, url):
    msg = EmailMessage()
    msg['Subject'] = f"Phishing Report - {country}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    msg.set_content(f"""To {team} ({country}),

I would like to report a phishing website:

{url}

This site appears to impersonate legitimate services and is collecting sensitive user information fraudulently.

Please take appropriate action under your national cybersecurity policy.

Sincerely,
{ORG_NAME}
Contact: {SENDER_EMAIL}
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[+] Email sent to {country}'s {team}.")
    except Exception as e:
        print(f"[!] Failed to email {country}'s {team}: {e}")

# === Web Form Opener Function ===
def open_form(team, country, url):
    print(f"[*] Opening form for {country}'s {team}...")
    webbrowser.open(url)

# === Main Function ===
def report_to_all_certs(url):
    print(f"[+] Starting phishing report to national CERTs for URL: {url}")
    
    for cert in CERT_DATABASE:
        country = cert["country"]
        team = cert["team"]
        method = cert["method"]
        contact = cert["contact"]

        if method == "email":
            send_email(team, country, contact, url)
        elif method == "form":
            open_form(team, country, contact)
    print("[✓] Reporting completed to all national teams.")
