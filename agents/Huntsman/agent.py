import psutil
import os
import json
import time
import platform
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'huntsman_config.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'huntsman_alerts.log')
SCAN_INTERVAL = 300  # 5 minutes by default

# === Default suspicious processes and paths ===
DEFAULT_CONFIG = {
    "suspicious_processes": [
        "mimikatz.exe", "meterpreter.exe", "nc.exe", "powershell.exe", "netcat", "nmap"
    ],
    "critical_paths": [
        "C:/Windows/System32/", "/etc/"  # Windows and Linux examples
    ],
    "scan_interval": 300
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Huntsman] Failed to load config, using defaults. {e}")
    return DEFAULT_CONFIG

def log_alert(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} [Huntsman ALERT] {message}\n")
    print(f"[Huntsman] {message}")

def scan_processes(suspicious_list):
    print("[Huntsman] Scanning running processes...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and any(susp.lower() in proc.info['name'].lower() for susp in suspicious_list):
                log_alert(f"Suspicious process detected: PID={proc.info['pid']}, Name={proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def scan_critical_paths(paths):
    print("[Huntsman] Scanning critical paths for anomalies...")
    for path in paths:
        if os.path.exists(path):
            try:
                file_count = sum(len(files) for _, _, files in os.walk(path))
                if file_count > 1000:  # Example arbitrary threshold
                    log_alert(f"Unusual file count in {path}: {file_count} files detected.")
            except Exception as e:
                log_alert(f"Error scanning {path}: {e}")


def main():
    print("[Huntsman] Initializing...")
    os_type = platform.system()
    print(f"[Huntsman] Detected OS: {os_type}")

    config = load_config()
    scan_interval = config.get('scan_interval', SCAN_INTERVAL)

    while True:
        scan_processes(config['suspicious_processes'])
        scan_critical_paths(config['critical_paths'])
        time.sleep(scan_interval)

if __name__ == "__main__":
    main()
