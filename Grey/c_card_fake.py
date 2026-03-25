import random
import string
import time
import requests
from faker import Faker

class FakePaymentSubmitter:
    def __init__(self, target_url):
        self.target_url = target_url
        self.fake = Faker()
        
    def generate_fake_card(self):
        """Generate a fake credit card number"""
        card_types = ['Visa', 'MasterCard', 'Amex', 'Discover']
        card_type = random.choice(card_types)
        
        if card_type == 'Visa':
            prefix = '4'
            length = 16
        elif card_type == 'MasterCard':
            prefix = random.choice(['51', '52', '53', '54', '55'])
            length = 16
        elif card_type == 'Amex':
            prefix = random.choice(['34', '37'])
            length = 15
        elif card_type == 'Discover':
            prefix = random.choice(['6011', '622126-622925', '644-649', '65'])
            length = 16
            
        card_number = prefix + ''.join(random.choices(string.digits, k=length-len(prefix)))
        return card_number, card_type
        
    def generate_fake_payment_data(self):
        """Generate fake payment data"""
        card_number, card_type = self.generate_fake_card()
        
        payment_data = {
            'card_number': card_number,
            'card_type': card_type,
            'expiration_month': random.randint(1, 12),
            'expiration_year': random.randint(2023, 2028),
            'cvv': ''.join(random.choices(string.digits, k=3)),
            'name': self.fake.name(),
            'address': self.fake.address(),
            'city': self.fake.city(),
            'state': self.fake.state_abbr(),
            'zip': self.fake.zipcode(),
            'country': self.fake.country_code(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number(),
        }
        
        return payment_data
        
    def submit_fake_payment(self):
        """Submit fake payment data"""
        payment_data = self.generate_fake_payment_data()
        
        try:
            response = requests.post(self.target_url, data=payment_data)
            return response.status_code, response.text
        except Exception as e:
            return None, str(e)
            
    def run(self, num_submissions=10, delay_range=(1, 5)):
        """Run multiple fake payment submissions"""
        results = []
        for i in range(num_submissions):
            status_code, response_text = self.submit_fake_payment()
            results.append({
                "submission": i+1,
                "status_code": status_code,
                "response_length": len(response_text) if response_text else 0,
                "error": response_text if status_code is None else None
            })
            # Wait for a random delay between submissions
            delay = random.uniform(*delay_range)
            time.sleep(delay)
        return results

def run_fake_payment_submissions(url, num_submissions=10, delay_range=(1, 5)):
    """
    Takes a URL from main.py, runs fake payment submissions, returns results.
    """
    submitter = FakePaymentSubmitter(url)
    results = submitter.run(num_submissions=num_submissions, delay_range=delay_range)
    output = ""
    for r in results:
        output += f"\nSubmission {r['submission']}/{num_submissions}:\n"
        output += f"Status Code: {r['status_code']}\n"
        output += f"Response Length: {r['response_length']} chars\n"
        if r['error']:
            output += f"Error: {r['error']}\n"
    return output

# For direct CLI usage (optional)
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        output = run_fake_payment_submissions(target_url, num_submissions=20)
        print(output)
    else:
        print("Usage: python script.py <target_url>")