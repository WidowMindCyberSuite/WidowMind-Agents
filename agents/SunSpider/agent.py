import requests
import socket
import time
import json
import os
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'sunspider_config.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'sunspider_alerts.log')
SCAN_INTERVAL = 3600  # 1 hour by default

DEFAULT_CONFIG = {
    "enable_ip_lookup": True,
    "enable_dns_lookup": True,
    "scan_interval": 3600
}

WHOAMI_URL = "https://api.ipify.org"

# === Simulated external reputation check (can be expanded later) ===
def fake_reputation_check(ip):
    # TODO: Integrate real reputation service APIs (AbuseIPDB, etc.)
    suspicious_ips = ['1.2.3.4', '5.6.7.8']
    if ip in suspicious_ips:
        return False
    return True

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_CONFIG

def log_alert(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} [SunSpider ALERT] {message}\n")
    print(f"[SunSpider] {message}")

def get_public_ip():
    try:
        response = requests.get(WHOAMI_URL)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        log_alert(f"Error fetching public IP: {e}")
    return None

def perform_dns_lookup():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        log_alert(f"Local DNS resolved: Hostname={hostname}, IP={local_ip}")
    except Exception as e:
        log_alert(f"Error during DNS lookup: {e}")

def main():
    print("[SunSpider] Initializing...")
    config = load_config()
    interval = config.get('scan_interval', SCAN_INTERVAL)

    while True:
        if config.get("enable_ip_lookup", True):
            public_ip = get_public_ip()
            if public_ip:
                log_alert(f"Public IP detected: {public_ip}")
                if not fake_reputation_check(public_ip):
                    log_alert(f"WARNING: Public IP {public_ip} flagged as suspicious!")

        if config.get("enable_dns_lookup", True):
            perform_dns_lookup()

        time.sleep(interval)

if __name__ == "__main__":
    main()