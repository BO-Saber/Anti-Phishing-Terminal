#!/usr/bin/python3
"""
Auto-responding Bots in Phishing Chatboxes
Deploy bots to waste phisher's time.
"""

import time
import random
import threading

def bot_response():
    """Bot response function"""
    responses = [
        "Hello! How can I help you today?",
        "Welcome to our service!",
        "Thank you for contacting us!",
        "Your request has been received.",
        "Please wait while we process your request.",
        "We will get back to you shortly.",
        "Your inquiry has been logged.",
        "Thank you for your patience.",
        "Your request is being processed.",
        "Please provide more details."
    ]
    
    # Randomly select a response
    return random.choice(responses)

def simulate_chat():
    """Simulate a chat session"""
    print("[BOT] Starting chat simulation...")
    
    # Simulate chat duration
    for _ in range(5):
        # Wait between messages
        time.sleep(random.uniform(1, 3))
        
        # Send bot response
        response = bot_response()
        print(f"[BOT] {response}")
    
    print("[BOT] Chat simulation completed.")

def run_auto_bot(num_chats=3):
    """Run the auto bot for a given number of concurrent chats"""
    # Create multiple threads to simulate concurrent chats
    threads = []
    for _ in range(num_chats):
        t = threading.Thread(target=simulate_chat)
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
