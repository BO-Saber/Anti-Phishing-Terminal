import webbrowser
# === Generate the Google Safe Browsing form link ===
def report_to_google_safebrowsing(url):
    base_url = "https://safebrowsing.google.com/safebrowsing/report_phish/"
    print("[*] Opening Google Safe Browsing phishing report form...")
    webbrowser.open(base_url + f"?url={url}")

