import requests
import time
import sys
import re
import hashlib
import argparse
import logging
from urllib.parse import urljoin, urlparse

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

HEADERS = {
    "User-Agent": "CERT-KitScanner/1.0 (Gov-CERT)",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_page_content(url):
    """Fetch the HTML content of the phishing page."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve page content from {url} — {e}")
        return ""

def extract_assets(content, base_url):
    """Extract JavaScript, CSS, and image assets from HTML content."""
    js_pattern = re.compile(r'<script[^>]*src="([^"]+)"', re.IGNORECASE)
    css_pattern = re.compile(r'<link[^>]*href="([^"]+)"[^>]*rel="stylesheet"', re.IGNORECASE)
    img_pattern = re.compile(r'<img[^>]*src="([^"]+)"', re.IGNORECASE)

    scripts = {urljoin(base_url, src) for src in js_pattern.findall(content)}
    styles = {urljoin(base_url, href) for href in css_pattern.findall(content)}
    images = {urljoin(base_url, src) for src in img_pattern.findall(content)}

    logging.info(f"Discovered {len(scripts)} JS, {len(styles)} CSS, and {len(images)} image assets.")
    return list(scripts | styles | images)

def calculate_fingerprint(url):
    """Generate a consistent fingerprint based on sorted asset paths."""
    content = get_page_content(url)
    if not content:
        return None, []

    assets = extract_assets(content, url)
    if not assets:
        return None, []

    sorted_assets = sorted(assets)
    hash_obj = hashlib.sha256()
    for asset in sorted_assets:
        hash_obj.update(asset.encode())

    fingerprint = hash_obj.hexdigest()
    return fingerprint, sorted_assets

def classify_by_assets(assets):
    """Optional: Try to match known phishing kits by asset signature patterns."""
    known_patterns = {
        "apple": ["appleid", "apple_logo", "icloud"],
        "facebook": ["fbcdn", "graph.facebook"],
        "outlook": ["outlook", "microsoft", "live.com"],
        "generic-login": ["login", "auth", "signin"],
    }

    matched_tags = []
    for tag, keywords in known_patterns.items():
        if any(kw in asset.lower() for asset in assets for kw in keywords):
            matched_tags.append(tag)

    return matched_tags

def main():
    parser = argparse.ArgumentParser(description="CERT Phishing Kit Fingerprinter")
    parser.add_argument("url", help="Target phishing site URL")
    parser.add_argument("--output", help="Save fingerprint to file")
    args = parser.parse_args()

    logging.info(f"Initiating fingerprint scan on: {args.url}")
    
    fingerprint, assets = calculate_fingerprint(args.url)
    if fingerprint:
        print(f"\n[+] SHA-256 Fingerprint: {fingerprint}")
        print(f"[+] Total assets used for fingerprint: {len(assets)}")

        tags = classify_by_assets(assets)
        if tags:
            print(f"[+] Matched indicators: {', '.join(tags)}")
        else:
            print("[i] No known kit tags matched. Possibly custom or obfuscated.")

        if args.output:
            try:
                with open(args.output, "w") as f:
                    f.write(f"Fingerprint: {fingerprint}\n")
                    f.write("Assets:\n" + "\n".join(assets) + "\n")
                    if tags:
                        f.write("Tags: " + ", ".join(tags) + "\n")
                logging.info(f"Fingerprint and data saved to {args.output}")
            except IOError as e:
                logging.error(f"Failed to save fingerprint file: {e}")
    else:
        logging.warning("No assets found — possible redirection, cloaking, or empty kit.")

def fingerprint_kit(url):
    fingerprint, assets = calculate_fingerprint(url)
    tags = classify_by_assets(assets)
    return fingerprint, assets, tags