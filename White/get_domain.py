import whois
import socket
import sys
import json
from urllib.parse import urlparse


def get_domain(url):
    """
    Extracts the domain name from a given URL, normalizes it, and fetches ownership and DNS data.
    
    Args:
        url (str): The URL string to process.
        
    Returns:
        dict: A dictionary containing:
            - domain (str): The normalized domain (e.g., example.com).
            - ownership (dict): WHOIS data for the domain.
            - dns (dict): DNS records (A, MX, NS, etc.) for the domain.
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Remove 'www.' prefix if present
        if domain.startswith("www."):
            domain = domain[4:]

        # Fetch WHOIS data
        ownership = {}
        try:
            whois_data = whois.whois(domain)
            ownership = {
                "registrar": whois_data.registrar,
                "creation_date": str(whois_data.creation_date),
                "expiration_date": str(whois_data.expiration_date),
                "name_servers": whois_data.name_servers,
            }
        except Exception as e:
            ownership = {"error": f"Failed to fetch WHOIS data: {e}"}

        # Fetch DNS data
        dns = {}
        try:
            # A record (IPv4 address)
            a_record = socket.gethostbyname(domain)
            dns["A"] = a_record

            # MX records (Mail Exchange)
            mx_records = socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
            dns["MX"] = [record[4][0] for record in mx_records]

            # NS records (Name Servers)
            ns_records = socket.getaddrinfo(domain, 53, socket.AF_INET, socket.SOCK_DGRAM)
            dns["NS"] = [record[4][0] for record in ns_records]
        except Exception as e:
            dns = {"error": f"Failed to fetch DNS data: {e}"}

        return {
            "domain": domain,
            "ownership": ownership,
            "dns": dns,
        }
    except Exception as e:
        return {"error": f"Failed to parse domain: {e}"}

if __name__ == "__main__":
    import sys
    import json
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    result = get_domain(url)
    print(json.dumps(result, indent=2, default=str))