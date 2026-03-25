import requests
import time
import random
import string
import uuid

def create_honeytoken():
    """Create a unique honeytoken"""
    return {
        "token_id": str(uuid.uuid4()),
        "username": f"user_{random.randint(1000, 9999)}",
        "password": ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
        "email": f"{random.randint(1000, 9999)}@example.com",
        "created_at": time.time()
    }

def submit_to_phishing_site(url, honeytoken):
    """Submit honeytoken to phishing site"""
    try:
        response = requests.post(
            f"{url}/register", 
            data=honeytoken,
            timeout=10
        )
        if response.status_code == 200:
            print(f"[+] Successfully submitted honeytoken: {honeytoken['token_id']}")
        else:
            print(f"[!] Failed to submit: {response.status_code}")
    except Exception as e:
        print(f"[!] Error: {e}")

def run_honeytoken_submission(url):
    honeytoken = create_honeytoken()
    print(f"[+] Created honeytoken: {honeytoken['token_id']}")
    submit_to_phishing_site(url, honeytoken)
