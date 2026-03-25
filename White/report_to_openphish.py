import webbrowser


def report_to_openphish(url):
    submit_url = "https://openphish.com/submit.html"
    print("[*] Opening OpenPhish submission page...")
    webbrowser.open(submit_url)
    print("[✓] Please paste the following URL in the form:")
    print(url)

