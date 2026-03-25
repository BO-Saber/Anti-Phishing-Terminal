import webbrowser


def report_to_facebook(url):
    print("[*] Opening Facebook report pages...")
    print(f"[*] Report malicious link: {url}")
    webbrowser.open("https://www.facebook.com/help/contact/263149623790594")
