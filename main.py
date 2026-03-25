# ---General Modules---
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import os
from scanner import *
import re
import whois



# ---Module for each components---
from White.get_domain import get_domain
from White.legal_takedown_notice import legal_takedown_notice
from White.report_to_browser_vendors import report_to_vendors
from White.report_to_national_response_team import report_to_all_certs
from White.report_to_email_providers import report_to_email_providers
from White.report_to_google_safebrowsing import report_to_google_safebrowsing
from White.report_to_isp import report_to_isp
from White.report_to_openphish import report_to_openphish
from White.report_to_phishtank import report_to_phishtank
from White.report_to_registrar import report_to_registrar
from White.submit_deindex_request import submit_deindex_requests
from White.report_to_facebook import report_to_facebook
from White.report_to_cloud_providers import report_to_cloud_providers
from White.report_to_netcraft import report_to_netcraft
from White.report_to_x import report_to_x
from White.report_to_chrome_security_team import report_to_chrome_security_team
from White.report_to_mozilla import report_to_mozilla
from White.report_to_antivirus_vendors import report_to_av_vendors
from White.report_to_icann_abuse_contact import report_to_icann_abuse_contact
from White.report_to_secret_services import report_to_secret_services
from Grey.inject_fake_alert import inject_fake_alert 
from Grey.slow_get_flood import run_slow_get_flood
from Grey.alert_for_whoise import run_whois_monitor
from Grey.automated_fake_account import submit_fake_form
from Grey.mass_fake_login import run_mass_fake_login
#from Grey.open_redirect_tester import test_open_redirect
from Grey.form_flooding import flood_forms
from Grey.geo_track import get_geo_info_from_url
from Grey.se_report_auto import report_to_google_safe_browsing, generate_report
from Grey.junk_data import flood_junk_data, fetch_proxies, submit_form
from Grey.fingerprinting_phishing_kits import fingerprint_kit
from Grey.html_source_monitor import compare_html_sources
from Grey.honeytoken_submission import run_honeytoken_submission
from Grey.ss_collector import capture_screenshot
from Grey.auto_bot import run_auto_bot
from Grey.passive_recon import passive_directory_crawl
from Grey.shadow_server import run_passive_dns_shadow_detection
from Grey.c_card_fake import run_fake_payment_submissions
from Grey.cross_site_recon import run_cross_site_recon
from Black.reverse_shell import rse






# --- Global variables for the application state ---
pending_manual_email = False
pending_legal_notice_url = None
pending_form_flooding = False
pending_requests = None
pending_threads = None

pending_fake_account = False
pending_fake_account_email = None
pending_fake_account_password = None
pending_fake_account_step = None

pending_mass_login = False
pending_mass_login_username = None
pending_mass_login_password = None
pending_mass_login_submissions = None
pending_mass_login_threads = None
pending_mass_login_delay = None
pending_mass_login_step = None

pending_open_redirect = False
pending_open_redirect_params = None
pending_open_redirect_step = None

pending_junk_data = False
pending_junk_fields = None
pending_junk_submissions = None
pending_junk_step = None

pending_html_monitor = False
pending_html_monitor_url2 = None
pending_html_monitor_step = None
# --- Modern GUI Theme ---
BG_COLOR = "#000000"
FG_COLOR = "#39FF14"
BTN_COLOR = "#000000"
BTN_HOVER = "#00b140"
BTN_TEXT = "#39FF14"
BORDER_COLOR = "#00b140"
FONT = ("Consolas", 12, "bold")
TITLE_FONT = ("Consolas", 20, "bold")
prompt_text = ">>> "  
input_start_index = None 


# Action description dictionaries 

action_descriptions1 = {
    "Get Domain": "Fetch ownership and DNS data for the phishing domain.",
    "Legal Takedown Notice": "Send legal notice to hosting provider to remove the site.",
    "Report To Browser Vendors": "Notify Chrome, Firefox, and other browser security teams.",
    "Report To National Response Team": "Report phishing attempts to national cyber security team.",
    "Report To Email Providers": "Alert email providers used by phishers.",
    "Report To Google Safebrowsing": "Submit the URL to Google’s Safe Browsing blacklist.",
    "Report To Isp": "Inform the Internet Service Provider hosting the phishing site.",
    "Report To Openphish": "Submit phishing URLs to OpenPhish.",
    "Report To Phishtank": "Report to PhishTank for public blacklist registration.",
    "Report To Registrar": "Report to the domain registrar of the phishing site.",
    "Submit Deindex Request": "Ask search engines to deindex the malicious site.",
    "Report To Facebook": "Report links or accounts on Facebook.",
    "Report To Cloud Providers": "Submit reports via cloud providers security channels.",
    "Report To Netcraft": "Notify Netcraft to investigate and block the phishing.",
    "Report To X": "Report malicious x or accounts.",
    "Report To Chrome Security Team": "Directly alert the Chrome team about phishing.",
    "Report To Mozilla": "Alert Mozilla for Firefox-based phishing defense.",
    "Report To Antivirus Vendors": "Inform AV companies to flag the site.",
    "Report To ICANN Abuse Contact": "Notify ICANN of abuse through the contact registry.",
    "Report To Secret Services": "Report to all the secret agencies all over the world."
}

white_actions = list(action_descriptions1.keys())

# Grey and Black Actions
action_descriptions2 = {
    "Form Flooding (Credential Pollution)": "Send junk data to phishing forms to corrupt stolen credentials.",
    "Fake Block Alert Injection": "Inject fake security warnings whenever the victims tries to fill up their details.",
    "Passive Reconnaissance (Directory crawling)": "Scan site structure without interacting.",
    "Light Server Clogging (Low-rate GET flood)": "Subtly overload server with slow traffic.",
    "Automated WHOIS Scanning & Email Alerts": "Track WHOIS changes and send auto alerts.",
    "Automated Fake Account Creation (Bot traps)": "Create fake accounts to pollute attacker’s DB.",
    "Mass Fake Login Attempts (to pollute data)": "Overload phishing DB with random credentials.",
    "Open Redirect Hijacking (reusing phisher’s flaws)": "Exploit open redirect on phishing site.",
    "Search Engine Reporting Automation": "Automate reports to search engines for blacklisting.",
    "Auto-filling Phishing Forms with Junk Data": "Auto-send random data to phisher's form.",
    "Fingerprinting Phishing Kits (unique asset detection)": "Identify kit using its unique assets.",
    "HTML Source Monitoring for Kit Similarities": "Track reused phishing kits via HTML code.",
    "Honeytoken Submission (track phishing backend)": "Submit trackable data to monitor attacker use.",
    "Screenshot Collection & Public Archiving": "Capture phishing site and store publicly.",
    "Auto-responding Bots in Phishing Chatboxes": "Deploy bots to waste phisher's time.",
    "Fake Payment or Credit Card Submissions (sandboxed)": "Simulate card input to pollute logs.",
    "Cross-Site Recon (checking same kit on other domains)": "Scan for same kits on other domains.",
    "AI-Based Cloning Detector & Alert System": "Detect site clones using AI.",
    "IP/Geo Tracking of the Phishing Site Host": "Find out where the phishing server is hosted.",
    "Passive DNS Logging & Shadow Server Detection": "Check historical DNS logs for shadow servers."
}

grey_actions = list(action_descriptions2.keys())

action_descriptions3 = {
    "Distributed Denial-of-Service (DDoS)": "Take down phishing site by overwhelming its server.",
    "Server Exploitation (e.g., RCE, SQLi, file upload vulnerabilities)": "Exploit server flaws to gain access.",
    "Malware Injection (worms, backdoors, trojans on phishing servers)": "Install malicious tools on server.",
    "Domain Hijacking (taking over phishing domain control via exploits)": "Take over domain via vulnerabilities.",
    "DNS Cache Poisoning (redirecting phishing traffic)": "Tamper with DNS to mislead users.",
    "Email Bombing (spamming phishing inbox with junk)": "Flood their email systems with noise.",
    "Credential Honeypot Hijack (stealing phishing victims' info from kits)": "Steal data from poorly secured kits.",
    "Reverse Shell Implantation (gaining remote control of phishing server)": "Gain persistent backdoor access.",
    "FTP/SSH Brute Force Attack": "Crack login credentials to server.",
    "Data Corruption or File Deletion (on the attacker’s server)": "Delete or alter attacker’s files.",
    "Botnet-Based Server Overload": "Use botnets to flood the phishing server.",
    "Phishing the Phisher (counter-phishing their panel)": "Steal phisher’s credentials from their panel.",
    "Poisoning their Analytics / Logs (e.g., injecting garbage into DB)": "Insert false data into attacker’s logs.",
    "Blacklist Forging (falsely reporting legitimate competitors as phishing)": "Abuse blacklists unethically.",
    "Cryptocurrency Drain Attack (if phishing page handles wallets)": "Drain crypto wallets tied to the phishing page.",
    "CMS Exploits (e.g., exploiting WordPress/Joomla plugins used by attacker)": "Exploit known CMS plugin flaws.",
    "SSL Certificate Forgery or Revocation Abuse": "Exploit cert issuance or force revocation.",
    "Hosting Provider Exploits (targeting weak admin panels)": "Access attacker’s host via provider flaws.",
    "Crashing Control Panels with Malformed Requests": "Crash the admin panel with bad payloads.",
    "Lawless “Hack Back” (taking the phishing site offline via force)": "Offensive retaliatory hacking."
}

black_actions = list(action_descriptions3.keys())

# File Name
def action_to_filename(action):
    # Convert action name to safe filename
    fname = re.sub(r'[^a-zA-Z0-9]', '_', action).lower()
    fname = re.sub(r'_+', '_', fname).strip('_') + ".py"
    if action == "Get Domain":
        return "get_domain.py"
    elif action == "Legal Takedown Notice":
        return "legal_takedown_notice.py"
    elif action == "Report To Browser Vendors":
        return "report_to_browser_vendors.py"
    elif action == "Report To National Response Team":
        return "report_to_national_response_team.py"
    elif action == "Report To Email Providers":
        return "report_to_email_providers.py"
    elif action == "Report To Google Safebrowsing":
        return "report_to_google_safebrowsing.py"
    elif action == "Report To Isp":
        return "report_to_isp.py"
    elif action == "Report To Openphish":
        return "report_to_openphish.py" 
    elif action == "Report To Phishtank":
        return "report_to_phishtank.py"
    elif action == "Report To Registrar":
        return "report_to_registrar.py"
    elif action == "Submit Deindex Request":
        return "submit_deindex_request.py"
    elif action == "Report To Facebook":  
        return "report_to_facebook.py"
    elif action == "Report To Cloud Providers":
        return "report_to_cloud_providers.py"
    elif action == "Report To Netcraft":
        return "report_to_netcraft.py"
    elif action == "Report To X":
        return "report_to_x.py"
    elif action == "Report To Chrome Security Team":
        return "report_to_chrome_security_team.py"
    elif action == "Report To Mozilla":
        return "report_to_mozilla.py"
    elif action == "Report To Antivirus Vendors":
        return "report_to_antivirus_vendors.py"
    elif action == "Report To ICANN Abuse Contact":
        return "report_to_icann_abuse_contact.py"
    elif action == "Report To Secret Services":
        return "report_to_secret_services.py"
    elif action == "Form Flooding (Credential Pollution)":
        return "form_flooding.py"
    elif action == "Fake Block Alert Injection":
        return "inject_fake_alert.py"
    elif action == "Passive Reconnaissance (Directory crawling)":
        return "passive_recon.py"
    elif action == "Light Server Clogging (Low-rate GET flood)":
        return "slow_get_flood.py"
    elif action == "Automated WHOIS Scanning & Email Alerts":
        return "whois_monitor.py"
    elif action == "Automated Fake Account Creation (Bot traps)":
        return "automated_fake_account.py"
    elif action == "Mass Fake Login Attempts (to pollute data)":
        return "mass_fake_login.py"
    elif action == "Open Redirect Hijacking (reusing phisher’s flaws)":
        return "open_redirect_tester.py"
    elif action == "Search Engine Reporting Automation":
        return "se_report_auto.py"
    elif action == "Auto-filling Phishing Forms with Junk Data":
        return "junk_data.py"
    elif action == "Fingerprinting Phishing Kits (unique asset detection)":
        return "fingerprinting_phishing_kits.py"
    elif action == "HTML Source Monitoring for Kit Similarities":
        return "html_source_monitor.py"
    elif action == "Honeytoken Submission (track phishing backend)":
        return "honeytoken_submission.py"
    elif action == "Screenshot Collection & Public Archiving":  
        return "ss_collector.py"
    elif action == "Auto-responding Bots in Phishing Chatboxes":
        return "auto_bot.py"
    elif action == "Passive DNS Logging & Shadow Server Detection":
        return "shaddow_server.py"
    elif action == "Geo Tracking":
        return "geo_track.py"
    elif action =="Fake Payment or Credit Card Submissions (sandboxed)":
        return "c_card_fake.py"
    elif action == "Cross-Site Recon":
        return "cross_site_recon.py"
    elif action == "Reverse Shell Implantation (gaining remote control of phishing server)":
        return "reverse_shell.py"
    else:
        return fname  # fallback, shouldn't happen

# Terminal Input Handling
def show_prompt():
    global input_start_index
    output_text.insert(tk.END, ">>> ")
    output_text.see(tk.END)
    input_start_index = output_text.index("end-1c")  # Save where user input starts

# Add this global variable at the top (with your other globals)
pending_terminal_step = None  # can be "requests", "threads", or None

# Replace your on_enter_terminal_input function with:
def on_enter_terminal_input(event):
    global input_start_index
    # Get only what the user typed after the prompt
    user_input = output_text.get(input_start_index, "end-1c").strip()
    # Remove the newline that pressing Enter would normally add
    output_text.delete("end-1c", tk.END)
    output_text.insert(tk.END, "\n")
    process_terminal_input(user_input)
    if not pending_form_flooding:
        show_prompt()
    return "break"
# Function to process terminal input commands


# Update your process_terminal_input function as follows:
def process_terminal_input(command):
    global pending_form_flooding, pending_requests, pending_threads, pending_terminal_step
    global pending_manual_email, pending_legal_notice_url
    global pending_fake_account, pending_fake_account_email, pending_fake_account_password, pending_fake_account_step
    global pending_mass_login, pending_mass_login_username, pending_mass_login_password, pending_mass_login_submissions, pending_mass_login_threads, pending_mass_login_delay, pending_mass_login_step
    global pending_open_redirect, pending_open_redirect_params, pending_open_redirect_step
    command = command.strip()
    url = entry.get().strip()
    print(f"DEBUG: command={repr(command)}")  # For debugging
    if pending_manual_email:
        # User is entering manual email for legal takedown
        url = pending_legal_notice_url
        from White.legal_takedown_notice import legal_takedown_notice
        result = legal_takedown_notice(
            url,
            "official.blackops.isf@gmail.com",
            "#Blackops3.0-isf",
            manual_email=command
        )
        output_text.insert(tk.END, "--- [Legal Takedown Notice] ---\n")
        output_text.insert(tk.END, result + "\n")
        pending_manual_email = False
        pending_legal_notice_url = None
        show_prompt()
        return
    # Only print [Executing] for normal commands, not for pending input
    if not pending_form_flooding or (pending_form_flooding and pending_terminal_step is None):
        output_text.insert(tk.END, f"[Executing] {command}\n")
        output_text.see(tk.END)
    try:
        if pending_form_flooding:
            if pending_terminal_step == "requests":
                try:
                    num = int(command)
                    if not (1 <= num <= 1000):
                        output_text.insert(tk.END, "[!] Please enter a valid number between 1 and 1000.\n")
                        show_prompt()
                        return
                    pending_requests = num
                    pending_terminal_step = "threads"
                    output_text.insert(tk.END, "Enter max threads (limit 20):\n")
                    show_prompt()  
                except Exception:
                    output_text.insert(tk.END, "[!] Please enter a valid number between 1 and 1000.\n")
                    show_prompt()
                return
            if pending_terminal_step == "threads":
                try:
                    num = int(command)
                    if not (1 <= num <= 20):
                        output_text.insert(tk.END, "[!] Please enter a valid number between 1 and 20.\n")
                        show_prompt()  # <-- Add this line
                        return
                    pending_threads = num
                    url = entry.get().strip()
                    import io
                    import contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        flood_forms(url, num_requests=pending_requests, max_threads=pending_threads)
                    result = buf.getvalue()
                    output_text.insert(tk.END, "--- [Form Flooding] ---\n")
                    output_text.insert(tk.END, result + "\n")
                except Exception:
                    output_text.insert(tk.END, "[!] Please enter a valid number between 1 and 20.\n")
                    show_prompt()  # <-- Add this line
                    return
                # Reset state after execution
                pending_form_flooding = False
                pending_requests = None
                pending_threads = None
                pending_terminal_step = None
                return
    except Exception as e:
        output_text.insert(tk.END, f"[!] Error: {e}\n")
    
    # --- Automated Fake Account Creation ---
    if pending_fake_account:
        if pending_fake_account_step == "email":
            pending_fake_account_email = command
            output_text.insert(tk.END, "Enter password field name:\n")
            pending_fake_account_step = "password"
            show_prompt()
            return
        elif pending_fake_account_step == "password":
            pending_fake_account_password = command
            import io, contextlib, time
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                for i in range(50):
                    submit_fake_form(url, pending_fake_account_email, pending_fake_account_password)
                    time.sleep(1)
            output = buf.getvalue()
            output_text.insert(tk.END, "--- [Automated Fake Account Creation] ---\n")
            output_text.insert(tk.END, output + "\n")
            # Reset state
            pending_fake_account = False
            pending_fake_account_email = None
            pending_fake_account_password = None
            pending_fake_account_step = None
            show_prompt()
            return

    # --- Mass Fake Login Attempts ---
    if pending_mass_login:
        if pending_mass_login_step == "username":
            pending_mass_login_username = command
            output_text.insert(tk.END, "Enter password field name:\n")
            pending_mass_login_step = "password"
            show_prompt()
            return
        elif pending_mass_login_step == "password":
            pending_mass_login_password = command
            output_text.insert(tk.END, "Enter number of submissions:\n")
            pending_mass_login_step = "submissions"
            show_prompt()
            return
        elif pending_mass_login_step == "submissions":
            try:
                pending_mass_login_submissions = int(command)
            except Exception:
                output_text.insert(tk.END, "[!] Please enter a valid number for submissions.\n")
                show_prompt()
                return
            output_text.insert(tk.END, "Enter number of threads:\n")
            pending_mass_login_step = "threads"
            show_prompt()
            return
        elif pending_mass_login_step == "threads":
            try:
                pending_mass_login_threads = int(command)
            except Exception:
                output_text.insert(tk.END, "[!] Please enter a valid number for threads.\n")
                show_prompt()
                return
            output_text.insert(tk.END, "Enter delay between requests (seconds):\n")
            pending_mass_login_step = "delay"
            show_prompt()
            return
        elif pending_mass_login_step == "delay":
            try:
                pending_mass_login_delay = float(command)
            except Exception:
                output_text.insert(tk.END, "[!] Please enter a valid number for delay.\n")
                show_prompt()
                return
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                run_mass_fake_login(
                    url,
                    username_field=pending_mass_login_username,
                    password_field=pending_mass_login_password,
                    num_submissions=pending_mass_login_submissions,
                    threads=pending_mass_login_threads,
                    delay_between=pending_mass_login_delay
                )
            output = buf.getvalue()
            output_text.insert(tk.END, "--- [Mass Fake Login Attempts] ---\n")
            output_text.insert(tk.END, output + "\n")
            # Reset state
            pending_mass_login = False
            pending_mass_login_username = None
            pending_mass_login_password = None
            pending_mass_login_submissions = None
            pending_mass_login_threads = None
            pending_mass_login_delay = None
            pending_mass_login_step = None
            show_prompt()
            return
        
    # --- Open Redirect Hijacking ---
'''    if pending_open_redirect:
        if pending_open_redirect_step == "params":
            pending_open_redirect_params = [p.strip() for p in command.split(",") if p.strip()]
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                test_open_redirect(url, pending_open_redirect_params)
            output = buf.getvalue()
            output_text.insert(tk.END, "--- [Open Redirect Hijacking] ---\n")
            output_text.insert(tk.END, output + "\n")
            # Reset state
            pending_open_redirect = False
            pending_open_redirect_params = None
            pending_open_redirect_step = None
            show_prompt()
            return
'''



# Script Runner Function
import subprocess
import threading
import time


# In your run_selected_actions, set the step variable:
def run_selected_actions():
    global pending_form_flooding, pending_requests, pending_threads, pending_terminal_step
    global pending_form_flooding, pending_requests, pending_threads, pending_terminal_step
    global pending_fake_account, pending_fake_account_email, pending_fake_account_password, pending_fake_account_step
    global pending_mass_login, pending_mass_login_username, pending_mass_login_password, pending_mass_login_submissions, pending_mass_login_threads, pending_mass_login_delay, pending_mass_login_step
    global pending_open_redirect, pending_open_redirect_params, pending_open_redirect_step
    global pending_junk_data, pending_junk_fields, pending_junk_submissions, pending_junk_step
    global pending_html_monitor, pending_html_monitor_url2, pending_html_monitor_step
    output_text.config(state="normal")
    selected = []
    url = entry.get().strip()
    for action, var in {**white_vars, **grey_vars, **black_vars}.items():
        if var.get():
            selected.append(action)
    if not selected:
        output_text.insert(tk.END, "No actions selected.\n")
        output_text.config(state="disabled")
        return
    if "Form Flooding (Credential Pollution)" in selected:
        pending_form_flooding = True
        pending_requests = None
        pending_threads = None
        pending_terminal_step = "requests"
        output_text.insert(tk.END, "Enter the number of requests (max 1000):\n")
        show_prompt()  # <-- Add this line after every custom prompt!
        output_text.see(tk.END)
        return
    # --- Automated Fake Account Creation ---
    if "Automated Fake Account Creation (Bot traps)" in selected:
        pending_fake_account = True
        pending_fake_account_email = None
        pending_fake_account_password = None
        pending_fake_account_step = "email"
        output_text.insert(tk.END, "Enter email field name:\n")
        show_prompt()
        output_text.see(tk.END)
        return
        # --- Mass Fake Login Attempts ---
    if "Mass Fake Login Attempts (to pollute data)" in selected:
        pending_mass_login = True
        pending_mass_login_username = None
        pending_mass_login_password = None
        pending_mass_login_submissions = None
        pending_mass_login_threads = None
        pending_mass_login_delay = None
        pending_mass_login_step = "username"
        output_text.insert(tk.END, "Enter username field name:\n")
        show_prompt()
        output_text.see(tk.END)
        return
    # --- Open Redirect Hijacking ---
    if "Open Redirect Hijacking (reusing phisher’s flaws)" in selected:
        pending_open_redirect = True
        pending_open_redirect_params = None
        pending_open_redirect_step = "params"
        output_text.insert(tk.END, "Enter comma-separated redirect parameter names (e.g. redirect,url,next,r,return,dest,redir,continue,goto):\n")
        show_prompt()
        output_text.see(tk.END)
        return
    # --- Auto-filling Phishing Forms with Junk Data ---
    if "Auto-filling Phishing Forms with Junk Data" in selected:
        pending_junk_data = True
        pending_junk_fields = None
        pending_junk_submissions = None
        pending_junk_step = "fields"
        output_text.insert(tk.END, "Enter comma-separated field names for the form:\n")
        show_prompt()
        output_text.see(tk.END)
        return  
    # --- HTML Source Monitoring for Kit Similarities ---
    if "HTML Source Monitoring for Kit Similarities" in selected:
        pending_html_monitor = True
        pending_html_monitor_url2 = None
        pending_html_monitor_step = "url2"
        output_text.insert(tk.END, "Enter the second URL to compare with:\n")
        show_prompt()
        output_text.see(tk.END)
        return            
    def run_scripts():
        global pending_manual_email, pending_legal_notice_url
        for action in selected:
            loading_index = output_text.index(tk.END)
            output_text.insert(tk.END, f"\n---[Processing... Please wait.]\n")
            output_text.see(tk.END)
            output_text.update()
            try:
                if action == "Get Domain":
                    import json
                    result = get_domain(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Get Domain Result] ---\n")
                    output_text.insert(tk.END, json.dumps(result, indent=2, default=str) + "\n")
                elif action == "Legal Takedown Notice":
                    result = legal_takedown_notice(
                        url,
                        "official.blackops.isf@gmail.com",
                        "#Blackops3.0-isf"
                    )
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    if result is None:
                        output_text.insert(tk.END, "[!] No abuse email found. Please type the abuse/hosting provider email address and press Enter:\n")
                        pending_manual_email = True
                        pending_legal_notice_url = url
                        show_prompt()
                        return  # Wait for user input
                    output_text.insert(tk.END, "--- [Legal Takedown Notice] ---\n")
                    output_text.insert(tk.END, result + "\n")
                elif action == "Report To Browser Vendors":
                    report_to_vendors(url)
                    output_text.insert(tk.END, "--- [Report To Browser Vendors] ---\n")
                    output_text.insert(tk.END, "[✓] Report process completed.\n")
                elif action == "Report To National Response Team":
                    import io
                    import contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        report_to_all_certs(url)
                    output = buf.getvalue()
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To National Response Team] ---\n")
                    output_text.insert(tk.END, output + "\n")
                elif action == "Report To Google Safebrowsing":
                    report_to_google_safebrowsing(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Google Safebrowsing] ---\n")
                    output_text.insert(tk.END, "[✓] Google Safe Browsing report form opened in browser.\n")
                elif action == "Report To Email Providers":
                    report_to_email_providers(url)
                    output_text.insert(tk.END, "--- [Report To Email Providers] ---\n")
                    output_text.insert(tk.END, "[✓] Report process completed.\n")
                elif action == "Report To Isp":
                    result = report_to_isp(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To ISP] ---\n")
                    output_text.insert(tk.END, result + "\n")
                elif action == "Report To Openphish":
                    report_to_openphish(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To OpenPhish] ---\n")
                    output_text.insert(tk.END, "[✓] OpenPhish submission page opened in browser. Please paste the URL in the form.\n")
                elif action == "Report To Phishtank":
                    report_to_phishtank(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To PhishTank] ---\n")
                    output_text.insert(tk.END, "[✓] PhishTank submission page opened in browser. Please paste the URL in the form.\n")
                elif action == "Report To Registrar":
                    report_to_registrar(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Registrar] ---\n")
                    output_text.insert(tk.END, result + "\n")
                elif action == "Submit Deindex Request":
                    submit_deindex_requests(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Submit Deindex Request] ---\n")
                    output_text.insert(tk.END, result + "\n")
                elif action == "Report To Facebook":
                    report_to_facebook(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Facebook] ---\n")
                    output_text.insert(tk.END, "[✓] Facebook report page opened in browser. Please submit the URL manually.\n")
                elif action == "Report To Cloud Providers":
                    result = report_to_cloud_providers(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Cloud Providers] ---\n")
                    output_text.insert(tk.END, result + "\n")
                elif action == "Report To Netcraft":
                    report_to_netcraft(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Netcraft] ---\n")
                    output_text.insert(tk.END, "[✓] Netcraft report page opened in browser. Please submit the URL manually.\n")
                elif action == "Report To X":
                    report_to_x(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To X] ---\n")
                    output_text.insert(tk.END, "[✓] X (Twitter) abuse report pages opened in browser. Please submit the URL manually.\n")
                elif action == "Report To Chrome Security Team":
                    report_to_chrome_security_team(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Chrome Security Team] ---\n")
                    output_text.insert(tk.END, "[✓] Chrome Security Team report form opened in browser. Please confirm the report by submitting the CAPTCHA.\n")
                elif action == "Report To Mozilla":
                    result = report_to_mozilla(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Mozilla] ---\n")
                    output_text.insert(tk.END, result + "\n")
                elif action == "Report To Antivirus Vendors":
                    report_to_av_vendors(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Antivirus Vendors] ---\n")
                    output_text.insert(tk.END, "[✓] Antivirus vendor report forms opened and emails sent where possible.\n")
                elif action == "Report To ICANN Abuse Contact":
                    result = report_to_icann_abuse_contact(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To ICANN Abuse Contact] ---\n")
                    output_text.insert(tk.END, result + "\n")
                elif action == "Report To Secret Services":
                    report_to_secret_services()
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Report To Secret Services] ---\n")
                    output_text.insert(tk.END, "[✓] Secret service/cybercrime agency portals opened in browser. Please submit the URL manually.\n")
                elif action == "Form Flooding (Credential Pollution)":
                    import io
                    import contextlib
                    try:
                        num_subs = int(entry_ff_subs.get())  # GUI entry field for submissions
                        num_threads = int(entry_ff_threads.get())  # GUI entry for threads
                    except ValueError:
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, "[!] Error: Invalid form flooding input (not integers).\n")
                        continue
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        flood_forms(url, num_requests=num_subs, max_threads=num_threads)
                    output = buf.getvalue()
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Form Flooding] ---\n")
                    output_text.insert(tk.END, output + "\n")
                elif action == "Fake Block Alert Injection":
                    try:
                        inject_fake_alert(url)
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, "--- [Fake Block Alert Injection] ---\n")
                        output_text.insert(tk.END, "[✓] Fake alert script injected. Start typing in any login field to trigger the alert. Browser will close after you press Enter in the console.\n")
                    except Exception as e:
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, f"[!] Error injecting fake alert: {e}\n")
                elif action == "Passive Reconnaissance (Directory crawling)":
                    output = passive_directory_crawl(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Passive Reconnaissance] ---\n")
                    output_text.insert(tk.END, output + "\n")
                elif action == "Light Server Clogging (Low-rate GET flood)":
                    try:
                        delay_sec = 2.0  # You can prompt the user for this value if you want
                        requests_per_thread = 10
                        num_threads = 5
                        import io
                        import contextlib
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            run_slow_get_flood(url, delay_sec, requests_per_thread, num_threads)
                        output = buf.getvalue()
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, "--- [Light Server Clogging] ---\n")
                        output_text.insert(tk.END, output + "\n")
                    except Exception as e:
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, f"[!] Error running slow GET flood: {e}\n")
                elif action == "Automated WHOIS Scanning & Email Alerts":
                    run_whois_monitor(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [WHOIS Monitor] ---\n")
                    output_text.insert(tk.END, "[✓] WHOIS monitoring started in the background. You will receive email alerts on changes.\n")
                elif action == "Automated Fake Account Creation (Bot traps)":
                    pending_fake_account = True
                    pending_fake_account_email = None
                    pending_fake_account_password = None
                    pending_fake_account_step = "email"
                    output_text.insert(tk.END, "Enter email field name:\n")
                    show_prompt()
                    output_text.see(tk.END)
                    return
                elif action == "Mass Fake Login Attempts (to pollute data)":
                    pending_mass_login = True
                    pending_mass_login_username = None
                    pending_mass_login_password = None
                    pending_mass_login_submissions = None
                    pending_mass_login_threads = None
                    pending_mass_login_delay = None
                    pending_mass_login_step = "username"
                    output_text.insert(tk.END, "Enter username field name:\n")
                    show_prompt()
                    output_text.see(tk.END)
                    return
                elif action == "Open Redirect Hijacking (reusing phisher’s flaws)":
                    pending_open_redirect = True
                    pending_open_redirect_params = None
                    pending_open_redirect_step = "params"
                    output_text.insert(tk.END, "Enter comma-separated redirect parameter names (e.g. redirect,url,next,r,return,dest,redir,continue,goto):\n")
                    show_prompt()
                    output_text.see(tk.END)
                    return
                elif action == "Search Engine Reporting Automation":
                    import io
                    import contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        result = report_to_google_safe_browsing(url)
                        generate_report(result)
                    output = buf.getvalue()
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Search Engine Reporting Automation] ---\n")
                    output_text.insert(tk.END, output + "\n")
                    output_text.insert(tk.END, "[✓] Google Safe Browsing report submitted. See generated report file for details.\n")
                elif action == "Auto-filling Phishing Forms with Junk Data":
                    if pending_junk_step == "fields":
                        pending_junk_fields = [f.strip() for f in entry.get().strip().split(",") if f.strip()]
                        output_text.insert(tk.END, "Enter number of submissions:\n")
                        pending_junk_step = "submissions"
                        show_prompt()
                        return
                    elif pending_junk_step == "submissions":
                        try:
                            pending_junk_submissions = int(entry_ff_subs.get())
                        except Exception:
                            output_text.insert(tk.END, "[!] Please enter a valid number for submissions.\n")
                            show_prompt()
                            return
                        import io, contextlib
                        from Grey.junk_data import flood_junk_data
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            flood_junk_data(
                                entry.get().strip(),
                                pending_junk_fields,
                                num_submissions=pending_junk_submissions,
                                use_proxies=True
                            )
                        output = buf.getvalue()
                        output_text.insert(tk.END, "--- [Junk Data Flooding] ---\n")
                        output_text.insert(tk.END, output + "\n")
                        # Reset state
                        pending_junk_data = False
                        pending_junk_fields = None
                        pending_junk_submissions = None
                        pending_junk_step = None
                        show_prompt()
                        return
                elif action == "Fingerprinting Phishing Kits (unique asset detection)":
                    import io
                    import contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        fingerprint, assets, tags = fingerprint_kit(url)
                        if fingerprint:
                            print(f"\n[+] SHA-256 Fingerprint: {fingerprint}")
                            print(f"[+] Total assets used for fingerprint: {len(assets)}")
                            if tags:
                                print(f"[+] Matched indicators: {', '.join(tags)}")
                            else:
                                print("[i] No known kit tags matched. Possibly custom or obfuscated.")
                        else:
                            print("[!] No assets found — possible redirection, cloaking, or empty kit.")
                    output = buf.getvalue()
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Phishing Kit Fingerprinting] ---\n")
                    output_text.insert(tk.END, output + "\n")
                elif action == "HTML Source Monitoring for Kit Similarities":
                    if pending_html_monitor_step == "url2":
                        # pending_html_monitor_url2 should already be set before this block
                        import io, contextlib
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            url1 = entry.get().strip()
                            url2 = pending_html_monitor_url2
                            similarity, combined_hash = compare_html_sources(url1, url2)
                            if similarity > 0:
                                print(f"Similarity: {similarity:.2%}")
                                print(f"Combined Hash: {combined_hash}")
                            else:
                                print("No significant similarity detected.")
                        output = buf.getvalue()
                        output_text.insert(tk.END, "--- [HTML Source Monitoring] ---\n")
                        output_text.insert(tk.END, output + "\n")
                        # Reset state
                        pending_html_monitor = False
                        pending_html_monitor_url2 = None
                        pending_html_monitor_step = None
                        show_prompt()
                        return
                elif action == "Honeytoken Submission (track phishing backend)":
                    import io
                    import contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        run_honeytoken_submission(url)
                    output = buf.getvalue()
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Honeytoken Submission] ---\n")
                    output_text.insert(tk.END, output + "\n")
                elif action == "Screenshot Collection & Public Archiving":
                    import io
                    import contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        capture_screenshot(url)
                    output = buf.getvalue()
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Screenshot Collection] ---\n")
                    output_text.insert(tk.END, output + "\n")
                elif action == "Auto-responding Bots in Phishing Chatboxes":
                    import io
                    import contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        run_auto_bot(num_chats=3)  # You can make num_chats configurable if you want
                    output = buf.getvalue()
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Auto-responding Bots] ---\n")
                    output_text.insert(tk.END, output + "\n")
                elif action == "IP/Geo Tracking of the Phishing Site Host":
                    import json
                    result = get_geo_info_from_url(url)
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, "--- [Geo Tracking Result] ---\n")
                    output_text.insert(tk.END, json.dumps(result, indent=2, default=str) + "\n")
                elif action == "Passive DNS Logging & Shadow Server Detection":
                    try:
                        suspicious, log_file = run_passive_dns_shadow_detection(url)
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, "--- [Passive DNS Logging & Shadow Server Detection] ---\n")
                        output_text.insert(tk.END, f"DNS logs exported to {log_file}\n")
                        if suspicious:
                            output_text.insert(tk.END, "Suspicious Domains:\n")
                            for domain, count in suspicious:
                                output_text.insert(tk.END, f"{domain} has {count} A records - possible shadow server\n")
                        else:
                            output_text.insert(tk.END, "No suspicious domains detected.\n")
                    except Exception as e:
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, f"[!] Error running Passive DNS detection: {e}\n")
                elif action == "Fake Payment or Credit Card Submissions (sandboxed)":
                    try:
                        import io
                        import contextlib
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            # You can make num_submissions configurable if you want
                            result = run_fake_payment_submissions(url, num_submissions=20)
                            print(result)
                        output = buf.getvalue()
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, "--- [Fake Payment/Credit Card Submissions] ---\n")
                        output_text.insert(tk.END, output + "\n")
                    except Exception as e:
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, f"[!] Error running Fake Payment Submissions: {e}\n")                
                elif action == "Cross-Site Recon (checking same kit on other domains)":
                    try:
                        import io
                        import contextlib
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            result = run_cross_site_recon(url)
                            print(result)
                        output = buf.getvalue()
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, "--- [Cross-Site Recon] ---\n")
                        output_text.insert(tk.END, output + "\n")
                    except Exception as e:
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, f"[!] Error running Cross-Site Recon: {e}\n")
                elif action == "Reverse Shell Implantation (gaining remote control of phishing server)":
                    if not os.path.exists("reverse_shell.py"):
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, "[!] Reverse shell script not found. Please ensure it exists.\n")
                        continue
                    import subprocess
                    try:
                        result = subprocess.run(
                            ["python", "reverse_shell.py"],
                            capture_output=True, text=True, timeout=120
                        )
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, "--- [Reverse Shell Result] ---\n")
                        output_text.insert(tk.END, result.stdout + "\n")
                        if result.stderr:
                            output_text.insert(tk.END, "[stderr]\n" + result.stderr + "\n")
                    except Exception as e:
                        output_text.config(state="normal")
                        output_text.delete(loading_index, tk.END)
                        output_text.insert(tk.END, f"[!] Error running reverse_shell.py: {e}\n")
                else:
                    output_text.config(state="normal")
                    output_text.delete(loading_index, tk.END)
                    output_text.insert(tk.END, f"Action '{action}' not implemented without subprocess.\n")
                output_text.insert(tk.END, "\n")
            except Exception as e:
                output_text.config(state="normal")
                output_text.delete(loading_index, tk.END)
                output_text.insert(tk.END, f"Error running {action}: {e}\n\n")
            output_text.config(state="disabled")
            output_text.see(tk.END)

    threading.Thread(target=run_scripts, daemon=True).start()


# Function to change button color on hover
def on_enter(e):
    e.widget['background'] = BTN_HOVER
    e.widget['foreground'] = BTN_TEXT

def on_leave(e):
    e.widget['background'] = BTN_COLOR
    e.widget['foreground'] = BTN_TEXT

def fade_in_tooltip(label, text, alpha=0):
    label.config(text=text)

def create_scrollable_action_frame(parent, title, color, actions, action_descriptions, vars_dict, checkbox_list):
    outer_frame = tk.LabelFrame(parent, text=title, font=FONT, fg=FG_COLOR, bg=color, bd=0, relief="flat", labelanchor="n")
    outer_frame.pack(side="left", fill="both", expand=True, padx=8, pady=8)

    canvas = tk.Canvas(outer_frame, bg=color, highlightthickness=0, bd=0)
    scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=color)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    select_all_var = tk.BooleanVar()
    def toggle_all():
        for var in vars_dict.values():
            var.set(select_all_var.get())

    select_all_cb = tk.Checkbutton(
        scrollable_frame, text="Select All", variable=select_all_var, command=toggle_all,
        font=FONT, bg=color, fg=FG_COLOR, selectcolor=color,
        activebackground=color, activeforeground=FG_COLOR, borderwidth=0
    )
    select_all_cb.pack(anchor="w", padx=10, pady=4)

    for action in actions:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(
            scrollable_frame, text=action.split(" (", 1)[0], variable=var, font=FONT,
            fg=FG_COLOR, bg=color, selectcolor=color,
            activebackground=color, activeforeground=FG_COLOR, borderwidth=0, highlightthickness=0
        )
        cb.pack(anchor="w", padx=10, pady=2)

        desc = action_descriptions.get(action, action)
        def make_enter(desc):
            return lambda event: fade_in_tooltip(tooltip, desc)
        def make_leave():
            return lambda event: tooltip.config(text="")
        cb.bind("<Enter>", make_enter(desc))
        cb.bind("<Leave>", make_leave())

        vars_dict[action] = var
        checkbox_list.append(cb)

    return outer_frame

# --- Functionality ---
def analyze():
    url = entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    if not url.startswith("http"):
        url = "http://" + url

    heuristics = check_url_heuristics(url)
    whois_result = is_registered_recently(url)
    gsb_result = check_google_safe_browsing(url)

    result_text = (
        f"[+] URL: {url}\n"
        f"[+] Heuristics: {heuristics}\n"
        f"[+] WHOIS: {whois_result}\n"
        f"[+] Google Safe Browsing: {gsb_result}\n"
    )

    output_text.config(state="normal")
    output_text.insert(tk.END, result_text + "\n" + "-"*50 + "\n")
    output_text.see(tk.END)
    output_text.config(state="disabled")

    #if "suspicious" in heuristics.lower() or "suspicious" in whois_result.lower() or "flagged" in gsb_result.lower():
    #    initiate_btn.config(state="normal")
    #else:
    #    initiate_btn.config(state="disabled")
    initiate_btn.config(state="normal")

# --- GUI Setup ---
root = tk.Tk()
root.title("⚔️ Anti-Phishing Analyzer & Eliminator")
root.state('zoomed')
root.configure(bg=BG_COLOR)
root.option_add("*Font", "{Segoe UI} 12 bold")

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)

header = tk.Label(main_frame, text="⚡ ANTI-PHISHING TERMINAL ⚡", font=TITLE_FONT, fg=FG_COLOR, bg=BG_COLOR)
header.pack(pady=(10, 5))

url_frame = tk.Frame(main_frame, bg=BG_COLOR)
ff_input_frame = tk.Frame(main_frame, bg=BG_COLOR)
url_frame.pack(padx=10, pady=10, fill="x")
tk.Label(url_frame, text="🔗 Enter Suspicious URL:", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(side="left", padx=(0, 8))
entry = tk.Entry(url_frame, font=FONT, bg="#232a34", fg=FG_COLOR, insertbackground=FG_COLOR, borderwidth=0, relief="flat", highlightthickness=2, highlightbackground=FG_COLOR)
entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

analyze_btn = tk.Button(url_frame, text="Analyze URL", font=FONT, bg=BTN_COLOR, fg=BTN_TEXT, activebackground=BTN_HOVER, activeforeground=BTN_TEXT, borderwidth=0, cursor="hand2", command=analyze)
analyze_btn.pack(side="left")
analyze_btn.bind("<Enter>", on_enter)
analyze_btn.bind("<Leave>", on_leave)

options_frame = tk.Frame(main_frame, bg=BG_COLOR)
options_frame.pack(fill="both", expand=True, padx=10)

white_vars, grey_vars, black_vars = {}, {}, {}
all_checkboxes = []

create_scrollable_action_frame(options_frame, "White Actions", BG_COLOR, white_actions, action_descriptions1, white_vars, all_checkboxes)
create_scrollable_action_frame(options_frame, "Grey Actions", BG_COLOR, grey_actions, action_descriptions2, grey_vars, all_checkboxes)
create_scrollable_action_frame(options_frame, "Black Actions", BG_COLOR, black_actions, action_descriptions3, black_vars, all_checkboxes)

log_frame = tk.Frame(main_frame, bg=BG_COLOR)
log_frame.pack(padx=10, pady=5, fill="both", expand=True)
# -- Entry fields for Form Flooding Params --

tk.Label(ff_input_frame, text="🧨 Fake Submissions:", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(side="left", padx=(0, 5))
entry_ff_subs = tk.Entry(ff_input_frame, width=5, font=FONT, bg="#232a34", fg=FG_COLOR, insertbackground=FG_COLOR, borderwidth=0, relief="flat")
entry_ff_subs.pack(side="left", padx=(0, 20))
entry_ff_subs.insert(0, "100")  # default

tk.Label(ff_input_frame, text="👤 Threads:", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(side="left", padx=(0, 5))
entry_ff_threads = tk.Entry(ff_input_frame, width=5, font=FONT, bg="#232a34", fg=FG_COLOR, insertbackground=FG_COLOR, borderwidth=0, relief="flat")
entry_ff_threads.pack(side="left")
entry_ff_threads.insert(0, "10")  # default

tooltip = tk.Label(log_frame, text="", font=("Segoe UI", 11), fg=FG_COLOR, bg=BG_COLOR, wraplength=950, justify="left")
tooltip.pack(pady=(5, 0))

initiate_btn = tk.Button(
    log_frame,
    text="🔥 INITIATE",
    font=FONT,
    bg=BTN_COLOR,
    fg=BTN_TEXT,
    activebackground=BTN_HOVER,
    activeforeground=BTN_TEXT,
    borderwidth=0,
    cursor="hand2",
    command=run_selected_actions  # <-- Connects the button to my runner
)
initiate_btn.pack(pady=5)
initiate_btn.bind("<Enter>", on_enter)
initiate_btn.bind("<Leave>", on_leave)
initiate_btn.config(state="disabled")

output_text = scrolledtext.ScrolledText(
    log_frame,
    state="normal",      # Allow typing
    bg="#000000",
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    font=("Consolas", 11),
    borderwidth=0,
    highlightthickness=0,
    wrap="word"
)
output_text.bind("<Return>", on_enter_terminal_input)

output_text.pack(pady=5, fill="both", expand=True)
output_text.tag_config("warn", foreground="#bfff00")
output_text.tag_config("success", foreground="#00b140")
show_prompt()
root.mainloop()

