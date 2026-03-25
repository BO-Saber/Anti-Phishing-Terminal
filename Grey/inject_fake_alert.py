from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import time
import sys
import re



# === Function to inject fake alert on phishing page ===
def inject_fake_alert(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        # Use webdriver-manager to install and manage ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except WebDriverException as e:
        print("[!] Failed to start Chrome WebDriver:", e)
        sys.exit(1)

    try:
        driver.get(url)
        print(f"[*] Opened: {url}")
        time.sleep(3)  # Let the page load

        # JavaScript injection for fake alert
        js_code = """
        (function(){
            function showFakeAlert() {
                alert("⚠️ Security Alert: Suspicious activity detected. Please verify your credentials.");
            }

            var inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');
            inputs.forEach(function(input) {
                input.addEventListener('input', function() {
                    if (!input.dataset.alertShown) {
                        showFakeAlert();
                        input.dataset.alertShown = 'true';
                    }
                });
            });
        })();
        """

        driver.execute_script(js_code)
        print("[✓] Fake alert script injected.")
        print("💡 Start typing in any login field to trigger the alert.")
        input("Press [Enter] to exit and close the browser...")

    finally:
        driver.quit()
        print("[*] Browser closed.")

