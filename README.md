# 🛡️ Anti-Phishing Terminal Tool

A powerful Python-based GUI application to analyze, detect, and disrupt phishing websites. Built for ethical use, this tool combines intelligent phishing detection heuristics with offensive countermeasures to combat malicious domains.

## 🚀 Features

- **URL Heuristic Analysis**
  - Suspicious keyword matching
  - Subdomain overuse detection
  - HTTPS & IP-based URL checks

- **WHOIS Domain Verification**
  - Registrar checks
  - Domain age filtering
  - Expiry and creation flags

- **Google Safe Browsing API Integration**
  - Real-time blacklist checks

- **Offensive Actions (Grey/Black Response Tools)**
  - 🔄 Form Flooding (Credential Pollution)
  - 🧵 Threaded Submission Attack
  - 📥 Fake Input Generator
  - 🛠️ DDoS Simulation (Under dev / ethical testing only)
  - 📩 Legal Takedown Template Generator

- **GUI Interface (Tkinter)**
  - Modern terminal-style interface
  - Dynamic component rendering (e.g., hidden fields show on action selection)
  - Console-like redirection for `input()` prompts

## 📂 Project Structure

├── main.py                    # Main GUI interface
├── get\_domain.py             # Extracts and validates domain
├── form\_flooding.py          # Fake credential submission script
├── legal\_takedown\_notice.py  # Generates legal complaint format
├── distribution\_denial\_of\_services.py  # Optional DoS module
├── scanner.py                # Phishing heuristics scanner
├── utils/                    # Helper scripts and shared logic
└── README.md

## 🧑‍💻 Usage

> **Requirements**:
> - Python 3.9+
> - Packages: `tkinter`, `requests`, `whois`, `validators`, `tldextract`, etc.

### 🔍 Example Workflow

1. Enter the URL to be analyzed.
2. Select an action (e.g., "Form Flooding").
3. Click `INITIATE`.
4. Depending on the action, dynamic inputs will appear (e.g., fake usernames, thread count).
5. Results are displayed in real-time on the GUI terminal.

## ✅ Legal & Ethical Notice

This tool is developed strictly for educational and ethical hacking purposes. Any offensive features (e.g., flooding, server overloads) should **only be used in controlled environments** with prior permission. Misuse of this tool may violate cybersecurity laws.

## 🙌 Credits

* Designed and developed by \Saber and his team
* Part of the **Black Ops Division**, ISF
* Inspired by real-world phishing attack patterns and cyber-defense tactics
