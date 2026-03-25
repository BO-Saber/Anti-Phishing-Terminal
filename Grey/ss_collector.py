import requests
import os
import time
import sys

# ScreenshotLayer or similar screenshot API
SCREENSHOT_API_KEY = "23267868979e6aba271e5f1fb1e810c6"
SCREENSHOT_API_URL = "https://api.screenshotlayer.com/api/capture"

def capture_screenshot(target_url, output_dir="./screenshots"):
    """Capture screenshot of phishing site using external API."""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = int(time.time())
        filename = f"{output_dir}/screenshot_{timestamp}.png"

        params = {
            "access_key": SCREENSHOT_API_KEY,
            "url": target_url,
            "viewport": "1920x1080",
            "format": "png"
        }

        print(f"[+] Requesting screenshot for {target_url}")
        response = requests.get(SCREENSHOT_API_URL, params=params, timeout=30)

        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"[✓] Screenshot saved as {filename}")
        else:
            print(f"[!] Failed to capture screenshot. Status code: {response.status_code}")
            print(f"    Response: {response.text}")

    except Exception as e:
        print(f"[!] Error capturing screenshot: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python screenshot_collector.py <TARGET_URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    capture_screenshot(target_url)

