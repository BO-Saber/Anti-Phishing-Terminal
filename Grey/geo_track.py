import socket
import requests
from urllib.parse import urlparse

def extract_domain_from_url(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except Exception as e:
        print(f"[!] Failed to parse URL: {e}")
        return None

def resolve_domain_to_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] Resolved {domain} to IP: {ip}")
        return ip
    except socket.gaierror:
        print(f"[!] Failed to resolve domain: {domain}")
        return None

def get_geo_info_fallback(ip):
    try:
        url = f"https://ipwho.is/{ip}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if not data.get("success", False):
            print(f"[!] Fallback geo lookup failed: {data.get('message', 'Unknown error')}")
            return {}

        return {
            "district": data.get("region"),  # closest approximation
            "offset": data.get("timezone", {}).get("offset"),
            "currency": data.get("currency", {}).get("code")
        }
    except Exception as e:
        print(f"[!] Fallback geo info error: {e}")
        return {}

def get_geo_info_free(ip):
    try:
        # ip-api with all supported fields
        url = f"http://ip-api.com/json/{ip}?fields=66846719"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data['status'] != 'success':
            print(f"[!] Geo lookup failed: {data.get('message', 'Unknown error')}")
            return None

        fallback_fields = get_geo_info_fallback(ip)
        data.update(fallback_fields)

        print(f"\n[+] Geo Info for {ip}:")
        for key, value in data.items():
            print(f"    {key}: {value}")

        return data
    except Exception as e:
        print(f"[!] Failed to retrieve geo info: {e}")
        return None

def get_geo_info_from_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    domain = extract_domain_from_url(url)
    if not domain:
        print("[!] Could not extract domain from URL.")
        return None
    ip = resolve_domain_to_ip(domain)
    if not ip:
        print("[!] Could not resolve domain to IP.")
        return None
    return get_geo_info_free(ip)
