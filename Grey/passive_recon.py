import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin

def normalize_url(url):
    """Ensure the URL has a scheme and no trailing slash."""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.rstrip("/")

def get_robots_txt(url):
    """Extract disallowed and allowed paths from robots.txt."""
    try:
        robots_url = urljoin(url, "/robots.txt")
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            disallowed = re.findall(r"Disallow:\s*(.*)", response.text)
            allowed = re.findall(r"Allow:\s*(.*)", response.text)
            return {"disallowed": disallowed, "allowed": allowed}
        return {"disallowed": [], "allowed": []}
    except Exception as e:
        print(f"[!] Error fetching robots.txt: {e}")
        return {"disallowed": [], "allowed": []}

def get_wayback_urls(domain):
    """Fetch archived URLs from Wayback Machine."""
    try:
        api = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey"
        response = requests.get(api, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [item[0] for item in data[1:]]  # Skip header
        return []
    except Exception as e:
        print(f"[!] Wayback Machine error: {e}")
        return []

def google_search_site(domain):
    """Use Google site: operator to find indexed links (scraped)."""
    try:
        query = f"site:{domain}"
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Detect block/interstitial page
            if ("enablejs" in response.text.lower() or
                "unusual traffic" in response.text.lower() or
                "detected unusual traffic" in response.text.lower()):
                print("[!] Google search blocked: Automated requests detected.")
                return "GOOGLE_BLOCKED"
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for a in soup.find_all("a", href=True):
                href = a['href']
                if "url?q=" in href and domain in href:
                    actual_url = re.search(r"url\?q=(https?://[^&]+)", href)
                    if actual_url:
                        results.append(actual_url.group(1))
            return results
        return []
    except Exception as e:
        print(f"[!] Google search error: {e}")
        return []

def bing_search_site(domain):
    """Use Bing site: operator to find indexed links (scraped)."""
    try:
        query = f"site:{domain}"
        url = f"https://www.bing.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for li in soup.find_all("li", {"class": "b_algo"}):
                a = li.find("a", href=True)
                if a and domain in a['href']:
                    results.append(a['href'])
            return results
        return []
    except Exception as e:
        print(f"[!] Bing search error: {e}")
        return []


def passive_directory_crawl(target_url):
    # Main function for passive directory discovery. Returns a string with results.
    output = []
    target_url = normalize_url(target_url)
    parsed = urlparse(target_url)
    domain = parsed.netloc
    output.append(f"\n[+] Passive scan for directories on: {domain}\n")
    # 1. robots.txt
    output.append("[*] Fetching robots.txt...")
    robots = get_robots_txt(target_url)
    disallowed = ', '.join(robots['disallowed']) if robots['disallowed'] else 'None'
    allowed = ', '.join(robots['allowed']) if robots['allowed'] else 'None'
    output.append(f"    [+] Disallowed paths: {disallowed}")
    output.append(f"    [+] Allowed paths: {allowed}")
    # 2. Wayback Machine
    output.append("\n[*] Fetching historical paths from Wayback Machine...")
    wayback = get_wayback_urls(domain)
    if wayback:
        output.append(f"    [+] Found {len(wayback)} URLs:")
        for url in wayback:
            output.append(f"       - {url}")
    else:
        output.append("    [!] No results from Wayback Machine.")
    # 3. Google site search
    output.append("\n[*] Checking Google indexed paths...")
    google_links = google_search_site(domain)
    if google_links == "GOOGLE_BLOCKED":
        output.append("    [!] Google blocked automated search requests. This is normal—Google does not allow scraping. Trying Bing instead...")
        bing_links = bing_search_site(domain)
        if bing_links:
            output.append(f"    [+] Found {len(bing_links)} Bing links:")
            for link in bing_links:
                output.append(f"       - {link}")
        else:
            output.append("    [!] No indexed paths found via Bing either.")
    elif not google_links:
        output.append("    [!] No indexed paths found via Google. Trying Bing...")
        bing_links = bing_search_site(domain)
        if bing_links:
            output.append(f"    [+] Found {len(bing_links)} Bing links:")
            for link in bing_links:
                output.append(f"       - {link}")
        else:
            output.append("    [!] No indexed paths found via Bing either.")
    else:
        output.append(f"    [+] Found {len(google_links)} Google links:")
        for link in google_links:
            output.append(f"       - {link}")
    return "\n".join(output) 