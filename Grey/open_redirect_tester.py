import requests
from urllib.parse import urlencode

def open_redirect(url, redirect_params):
    session = requests.Session()
    session.headers.update({"User-Agent": "OpenRedirectTester/1.1"})

    print(f"[*] Testing {url} for open redirect vulnerabilities...\n")

    for param in redirect_params:
        payload = {param: "https://www.google.com"}  # Fixed test domain
        test_url = f"{url}?{urlencode(payload)}"

        try:
            response = session.get(test_url, allow_redirects=False, timeout=5)
            status = response.status_code
            location = response.headers.get("Location", "")

            if 300 <= status < 400:
                if "redirect.test" in location:
                    print(f"[!] Vulnerable parameter found: '{param}'")
                    print(f"    ➜ Exploitable URL: {test_url}")
                    print(f"    ➜ Redirects to: {location}\n")
                else:
                    print(f"[-] Parameter '{param}' triggers redirect, but not to external site.")
                    print(f"    ➜ Location header: {location}\n")
            else:
                print(f"[✓] Parameter '{param}' does not trigger a redirect ({status} {response.reason})")

        except requests.RequestException as e:
            print(f"[X] Error testing parameter '{param}': {e}\n")

