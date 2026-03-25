import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import concurrent.futures

class KitScanner:
    def __init__(self, target_domain):
        self.target_domain = target_domain
        self.kits = set()
        self.found_kits = {}
        
    def extract_kit_info(self, url):
        """Extract kit information from a URL"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract common kit indicators
            kit_indicators = {
                'meta_generator': soup.find('meta', attrs={'name': 'generator'}).get('content') if soup.find('meta', attrs={'name': 'generator'}) else None,
                'script_srcs': [script.get('src') for script in soup.find_all('script') if script.get('src')],
                'link_hrefs': [link.get('href') for link in soup.find_all('link') if link.get('href')],
                'body_classes': soup.body.get('class') if soup.body else [],
            }
            
            return kit_indicators
        except Exception as e:
            print(f"Error extracting kit info from {url}: {str(e)}")
            return None
    
    def find_similar_kits(self, domain):
        """Find similar kits on a domain"""
        try:
            kit_info = self.extract_kit_info(f"http://{domain}")
            if not kit_info:
                return
            
            for indicator_type, indicators in kit_info.items():
                if not indicators:
                    continue
                    
                if indicator_type == 'meta_generator':
                    if any(kit.startswith(indicators) for kit in self.kits):
                        self.found_kits[domain] = kit_info
                        break
                        
                elif indicator_type in ['script_srcs', 'link_hrefs']:
                    for indicator in indicators:
                        if any(re.search(kit, indicator) for kit in self.kits):
                            self.found_kits[domain] = kit_info
                            break
                            
                elif indicator_type == 'body_classes':
                    for kit in self.kits:
                        if any(re.search(kit, cls) for cls in indicators):
                            self.found_kits[domain] = kit_info
                            break
                            
        except Exception as e:
            print(f"Error finding kits on {domain}: {str(e)}")
    
    def scan_domains(self, domains):
        """Scan multiple domains for kits"""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.find_similar_kits, domain) for domain in domains]
            for future in concurrent.futures.as_completed(futures):
                future.result()

def get_related_domains(domain):
    """Get related domains using various techniques"""
    # This is a simplified example - in practice, you would use more advanced techniques
    related_domains = [
        f"www.{domain}",
        f"mail.{domain}",
        f"blog.{domain}",
        f"shop.{domain}",
        f"admin.{domain}",
    ]
    
    # Add subdomains from search engines, etc.
    return related_domains

def run_cross_site_recon(url):
    """
    Takes a URL, extracts the domain, scans for similar phishing kits on related domains.
    Returns a summary string of found kits.
    """
    # Extract domain from URL
    parsed = urlparse(url)
    domain = parsed.netloc if parsed.netloc else url
    if domain.startswith("www."):
        domain = domain[4:]
    scanner = KitScanner(domain)
    # Get initial kit info from target domain
    scanner.extract_kit_info(f"http://{domain}")
    # Get related domains to scan
    domains_to_scan = get_related_domains(domain)
    # Scan domains for similar kits
    scanner.scan_domains(domains_to_scan)
    # Prepare results
    result = f"\nFound similar kits on {len(scanner.found_kits)} domains:\n"
    for domain, kit_info in scanner.found_kits.items():
        result += f"\nDomain: {domain}\nKit Info:\n"
        for indicator_type, indicators in kit_info.items():
            result += f"  {indicator_type}: {indicators}\n"
    if not scanner.found_kits:
        result += "No similar kits found on related domains.\n"
    return result

# For direct CLI usage (optional)
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(run_cross_site_recon(url))
    else:
        print("Usage: python cross_site_recon.py <url>")