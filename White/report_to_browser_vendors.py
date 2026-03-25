import webbrowser
import smtplib
from email.message import EmailMessage

# ---------- Configurable Info ----------
ORG_NAME = "Black Ops | ISF"
SENDER_EMAIL = "official.blackops.isf@gmail.com"
SENDER_PASSWORD = "your_app_password"  # App Password recommended
# ---------------------------------------

def open_web_form(name, url):
    print(f"[*] Opening report form for {name}...")
    webbrowser.open(url)

def send_email_report(vendor_name, recipient_email, url):
    print(f"[*] Sending email to {vendor_name}...")

    msg = EmailMessage()
    msg['Subject'] = "Phishing URL Report"
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    msg.set_content(f"""Hello {vendor_name} Security Team,

We have identified a phishing website:

{url}

This site impersonates legitimate services and attempts to steal user credentials.
Please review and take appropriate action.

Sincerely,
{ORG_NAME}
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[+] Email sent to {vendor_name}.")
    except Exception as e:
        print(f"[!] Failed to send email to {vendor_name}: {e}")


# List of browsers & their phishing report mechanisms
vendors = [
    {"name": "Google Chrome", "type": "form", "url_template": "https://safebrowsing.google.com/safebrowsing/report_phish/?url={url}"},
    {"name": "Brave", "type": "email", "email": "security@brave.com"},
    {"name": "Mozilla Firefox", "type": "email", "email": "abuse@mozilla.org"},
    {"name": "Microsoft Edge", "type": "form", "url_template": "https://feedback.smartscreen.microsoft.com/feedback.aspx?url={url}"},
    {"name": "Opera", "type": "form", "url": "https://www.opera.com/security/phishing-report"},
    {"name": "Vivaldi", "type": "form", "url": "https://vivaldi.com/bugreport/?category=Security"},
    {"name": "Samsung Internet", "type": "form", "url": "https://help.content.samsung.com/csweb/main/main.do"},
    {"name": "Tor Browser", "type": "form", "url": "https://support.torproject.org/abuse/"},
    {"name": "DuckDuckGo", "type": "form", "url": "https://duckduckgo.com/feedback"},
    {"name": "Puffin", "type": "form", "url": "https://support.cloudmosa.com/support/tickets/new"},
    {"name": "UC Browser", "type": "form", "url": "https://www.ucweb.com/contact"},
    {"name": "Maxthon", "type": "form", "url": "https://www.maxthon.com/mx/contact-us/"},
    {"name": "Comodo Dragon", "type": "form", "url": "https://www.comodo.com/contact/"},
    {"name": "Iridium", "type": "form", "url": "https://iridiumbrowser.de/contact/"},
    {"name": "Epic Browser", "type": "form", "url": "https://epicbrowser.com/contact.html"},
    {"name": "Waterfox", "type": "form", "url": "https://www.waterfox.net/contact/"},
    {"name": "Librewolf", "type": "form", "url": "https://librewolf.net/contact/"},
    {"name": "Yandex Browser", "type": "form", "url": "https://browser.yandex.com/support/common/troubleshooting/broken-site.html"},
]

def report_to_vendors(url):
    for vendor in vendors:
        if vendor["type"] == "form":
            form_url = vendor.get("url_template", vendor.get("url"))
            if "url_template" in vendor:
                form_url = vendor["url_template"].format(url=url)
            open_web_form(vendor["name"], form_url)
        elif vendor["type"] == "email":
            send_email_report(vendor["name"], vendor["email"], url)

