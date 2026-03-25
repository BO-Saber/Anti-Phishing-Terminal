import webbrowser

# === Search Engine Deindex URLs ===
DEINDEX_PORTALS = [
    {
        "name": "Google Safe Browsing",
        "url_template": "https://safebrowsing.google.com/safebrowsing/report_phish/?url={url}"
    },
    {
        "name": "Google Search Console Deindex (requires login)",
        "url": "https://search.google.com/search-console/remove-outdated-content"
    },
    {
        "name": "Bing Webmasters - Content Removal Tool",
        "url": "https://www.bing.com/webmaster/tools/contentremoval"
    },
    {
        "name": "Yandex Webmaster Report Spam",
        "url": "https://yandex.com/support/webmaster/troubleshooting/phishing.html"
    },
    {
        "name": "Baidu Security Reporting",
        "url": "https://security.baidu.com/report/url"
    }
]

# === Open in browser
def submit_deindex_requests(url):
    print("[*] Submitting deindexing requests for:", url)
    for engine in DEINDEX_PORTALS:
        if "url_template" in engine:
            page_url = engine["url_template"].format(url=url)
        else:
            page_url = engine["url"]
        print(f"[*] Opening {engine['name']} deindexing page...")
        webbrowser.open(page_url)


