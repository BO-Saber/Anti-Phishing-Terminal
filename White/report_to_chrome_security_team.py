import webbrowser

def report_to_chrome_security_team(url):
    print("[*] Opening Chrome Security (Google Safe Browsing) phishing report form...")
    webbrowser.open(f"https://safebrowsing.google.com/safebrowsing/report_phish/?url={url}")
    print(f"[✓] Please confirm the report by submitting the CAPTCHA on the opened page.")
