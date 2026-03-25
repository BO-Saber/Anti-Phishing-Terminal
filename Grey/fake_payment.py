import time 
def simulate_payment():
    """Simulates a payment transaction"""
    
    # Simulated payment data
    payment_data = {
        'card_number': '4111111111111111',  # Visa test card
        'expiry_month': '12',
        'expiry_year': '2025',
        'cvv': '123',
        'amount': '99.99',
        'currency': 'USD',
        'billing_address': {
            'street': '123 Main St',
            'city': 'Springfield',
            'state': 'IL',
            'postal_code': '62704',
            'country': 'USA'
        }
    }
    
    # Print payment data to simulate submission
    print("=== Payment Submission ===")
    for key, value in payment_data.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    
    # Simulate submission delay
    import time
    time.sleep(1)
    
    # Simulate successful submission
    print("Payment processed successfully!")

def main():
    """Main execution loop"""
    
    # Simulate multiple submissions
    for _ in range(5):
        simulate_payment()
        # Add delay between submissions
        time.sleep(0.5)

if __name__ == "__main__":
    main()