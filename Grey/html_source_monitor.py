import requests
import time
import sys
import re
import argparse
import difflib
import hashlib

def get_html_content(url):

    """Fetch HTML content."""
    try:
        response = requests.get(url, timeout=10)
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def get_key_elements(html):
    """Extract key elements from HTML."""
    # Remove comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # Extract key elements
    elements = []
    
    # Head elements
    head_content = re.search(r'<head>(.*?)</head>', html, re.DOTALL)
    if head_content:
        elements.append(head_content.group(1))
    
    # Body elements
    body_content = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if body_content:
        elements.append(body_content.group(1))
    
    return '\n'.join(elements)

def calculate_similarity(url1, url2):
    """Calculate similarity between two HTML sources."""
    content1 = get_html_content(url1)
    content2 = get_html_content(url2)
    
    if not content1 or not content2:
        return 0
    
    # Get key elements
    key1 = get_key_elements(content1)
    key2 = get_key_elements(content2)
    
    # Calculate similarity ratio
    similarity = difflib.SequenceMatcher(None, key1, key2).ratio()
    
    return similarity

def compare_html_sources(url1, url2):
    parser = argparse.ArgumentParser(description='HTML Source Monitoring Tool')
    parser.add_argument('url1', help='First target URL')
    parser.add_argument('url2', help='Second target URL')
    
    args = parser.parse_args()
    
    print(f"Comparing: {args.url1} vs {args.url2}")
    
    similarity = calculate_similarity(args.url1, args.url2)
    
    if similarity > 0:
        print(f"Similarity: {similarity:.2%}")
        
        # Generate hash for further analysis
        combined = f"{args.url1}:{args.url2}"
        combined_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        print(f"Combined Hash: {combined_hash}")
    else:
        print("No significant similarity detected.")
