import webbrowser
def report_to_phishtank(url):
    print("[*] Opening PhishTank submission page...")
    webbrowser.open("https://phishtank.org/submit.php")
    print("[✓] Please paste the following URL manually into the form:")
    print(url)

