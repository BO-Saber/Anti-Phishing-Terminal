import webbrowser


def report_to_x(url):
    print("[*] Opening X (Twitter) abuse reporting forms...")
    print(f"[*] Report phishing link: {url}")
    webbrowser.open("https://help.twitter.com/forms/spam")
    print("[*] Optionally report abuse or threats:")
    webbrowser.open("https://help.twitter.com/forms/abusiveuser")

