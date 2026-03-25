import requests
import json
from datetime import datetime

# Configuration
GOOGLE_SAFE_BROWSING_API_KEY = "YOUR_GOOGLE_API_KEY"
GOOGLE_SAFE_BROWSING_REPORT_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

def report_to_google_safe_browsing(url):
    """Report a single URL to Google Safe Browsing for blacklisting."""
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "client": {
            "clientId": "your-client-id",
            "clientVersion": "1.0",
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    params = {
        "key": GOOGLE_SAFE_BROWSING_API_KEY,
    }

    try:
        response = requests.post(
            GOOGLE_SAFE_BROWSING_REPORT_URL,
            headers=headers,
            params=params,
            data=json.dumps(payload),
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error reporting URL: {e}")
        return None


def generate_report(results):
    """Generate a report of the blacklisting results."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"blacklist_report_{timestamp}.txt"

    with open(report_filename, "w") as report_file:
        report_file.write(f"Blacklisting Report - {timestamp}\n")
        report_file.write("=" * 40 + "\n")
        if results:
            report_file.write(json.dumps(results, indent=2))
        else:
            report_file.write("No results or an error occurred during reporting.\n")

    print(f"Report generated: {report_filename}")


