import dns.resolver
import datetime
import csv
from collections import defaultdict

class PassiveDNSLogger:
    def __init__(self):
        self.dns_cache = defaultdict(list)
        
    def log_dns_query(self, domain, record_type='A'):
        """Log DNS queries to cache"""
        try:
            answers = dns.resolver.resolve(domain, record_type)
            for rdata in answers:
                timestamp = datetime.datetime.now().isoformat()
                self.dns_cache[domain].append({
                    'timestamp': timestamp,
                    'record_type': record_type,
                    'value': str(rdata),
                    'ttl': answers.rrset.ttl
                })
        except Exception as e:
            print(f"Error querying {domain}: {str(e)}")

    def export_logs(self, filename):
        """Export DNS logs to CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Domain', 'Timestamp', 'Record Type', 'Value', 'TTL'])
            for domain, entries in self.dns_cache.items():
                for entry in entries:
                    writer.writerow([
                        domain,
                        entry['timestamp'],
                        entry['record_type'],
                        entry['value'],
                        entry['ttl']
                    ])

class ShadowServerDetector:
    def __init__(self, dns_logger):
        self.dns_logger = dns_logger
        
    def detect_shadow_servers(self):
        """Analyze logs for shadow server patterns"""
        suspicious_domains = []
        
        for domain, entries in self.dns_logger.dns_cache.items():
            # Check for multiple A records (load balancing)
            a_records = set()
            for entry in entries:
                if entry['record_type'] == 'A':
                    a_records.add(entry['value'])
            
            if len(a_records) > 3:  # Threshold for suspicion
                suspicious_domains.append((domain, len(a_records)))
                
        return suspicious_domains

# Example usage as a function for main.py
def run_passive_dns_shadow_detection(url):
    """
    Takes a URL, extracts the domain, runs passive DNS logging and shadow server detection.
    Returns suspicious domains list and logs filename.
    """
    import re
    # Extract domain from URL
    domain_match = re.search(r"https?://([^/]+)", url)
    if domain_match:
        domain = domain_match.group(1)
    else:
        domain = url  # fallback, assume it's a domain

    logger = PassiveDNSLogger()
    # Log DNS queries for A, MX, TXT
    logger.log_dns_query(domain)
    logger.log_dns_query(domain, 'MX')
    logger.log_dns_query(domain, 'TXT')
    # Export logs
    log_file = "dns_logs.csv"
    logger.export_logs(log_file)
    # Detect shadow servers
    detector = ShadowServerDetector(logger)
    suspicious = detector.detect_shadow_servers()
    return suspicious, log_file

# If you want to keep CLI usage:
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        suspicious, log_file = run_passive_dns_shadow_detection(url)
        print(f"DNS logs exported to {log_file}")
        print("\nSuspicious Domains:")
        for domain, count in suspicious:
            print(f"{domain} has {count} A records - possible shadow server")
    else:
        print("Usage: python shaddow_server.py <URL>")