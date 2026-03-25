import requests
import random
import string
import time

# === CONFIG ===
NUMBER_OF_SUBMISSIONS = 50
DELAY_BETWEEN_REQUESTS = 1  # seconds

# === FAKE CREDENTIAL GENERATOR ===
def generate_fake_email():
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"])
    return f"{name}{random.randint(100,999)}@{domain}"

def generate_fake_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# === BOT TRAP ENGINE ===
def submit_fake_form(url, email_field, password_field):
    email = generate_fake_email()
    password = generate_fake_password()

    data = {
        email_field: email,
        password_field: password
    }

    try:
        response = requests.post(url, data=data, timeout=5)
        print(f"[+] Submitted fake account: {email} / {password} | Status: {response.status_code}")
    except Exception as e:
        print(f"[!] Failed to submit: {e}")

