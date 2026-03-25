import webbrowser

def report_to_netcraft(url):
    print("[*] Opening Netcraft phishing report portal...")
    webbrowser.open("https://report.netcraft.com/phishing")
    print("[✓] Please submit the following phishing URL in the Netcraft form:\n")
    print(url)

