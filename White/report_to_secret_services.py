import webbrowser

AGENCIES = [
    {"country": "USA", "agency": "FBI (IC3)", "url": "https://www.ic3.gov"},
    {"country": "UK", "agency": "NCSC / MI5", "url": "https://www.ncsc.gov.uk/section/about-this-website/report-scam-website"},
    {"country": "India", "agency": "MHA Cyber Crime", "url": "https://cybercrime.gov.in"},
    {"country": "Canada", "agency": "Canadian Anti-Fraud Centre", "url": "https://www.antifraudcentre-centreantifraude.ca"},
    {"country": "Australia", "agency": "AFP + ACSC", "url": "https://www.cyber.gov.au/report"},
    {"country": "Interpol", "agency": "Interpol Cybercrime", "url": "https://www.interpol.int/en/Crimes/Cybercrime/Report-cybercrime"}
]

def report_to_secret_services():
    print("[*] Opening cybercrime reporting portals for global security agencies...")
    for agency in AGENCIES:
        print(f"[→] {agency['country']} - {agency['agency']}")
        webbrowser.open(agency["url"])

