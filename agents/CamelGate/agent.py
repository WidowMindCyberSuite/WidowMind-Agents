import psutil
import socket
import time
import platform
import os
import json
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'camelgate_config.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'camelgate_alerts.log')
SCAN_INTERVAL = 10  # seconds between scans

# === Default thresholds if config missing ===
DEFAULT_THRESHOLDS = {
    "browser": 100 * 1024 * 1024,   # 100MB
    "shell": 5 * 1024 * 1024,       # 5MB
    "other": 20 * 1024 * 1024       # 20MB
}

BROWSER_PROCESSES = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'chrome', 'firefox', 'msedge']
SHELL_PROCESSES = ['cmd.exe', 'powershell.exe', 'bash', 'sh']
WHITELIST_IPS = ['8.8.8.8', '1.1.1.1']

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[CamelGate] Failed to load config, using defaults. {e}")
    return DEFAULT_THRESHOLDS

def log_alert(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} [CamelGate ALERT] {message}\n")
    print(f"[CamelGate] {message}")

def classify_process(proc_name):
    name = proc_name.lower()
    if name in (p.lower() for p in BROWSER_PROCESSES):
        return "browser"
    elif name in (p.lower() for p in SHELL_PROCESSES):
        return "shell"
    else:
        return "other"

def is_ip_whitelisted(ip):
    return ip in WHITELIST_IPS

def monitor_outbound():
    print("[CamelGate] Outbound monitor started...")
    thresholds = load_config()

    while True:
        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.status != psutil.CONN_ESTABLISHED:
                    continue
                if conn.raddr:
                    remote_ip = conn.raddr.ip
                    local_pid = conn.pid

                    if not is_ip_whitelisted(remote_ip):
                        try:
                            proc = psutil.Process(local_pid)
                            proc_name = proc.name()
                            io_counters = proc.io_counters()
                            bytes_sent = io_counters.bytes_sent

                            proc_class = classify_process(proc_name)
                            threshold = thresholds.get(proc_class, DEFAULT_THRESHOLDS[proc_class])

                            if bytes_sent > threshold:
                                log_alert(f"High outbound traffic! PID={local_pid}, EXE={proc_name}, SENT={bytes_sent/1024/1024:.2f} MB, Destination={remote_ip}, Class={proc_class}")

                        except Exception as e:
                            continue

        except Exception as scan_error:
            print(f"[CamelGate] Error scanning outbound connections: {scan_error}")

        time.sleep(SCAN_INTERVAL)

def main():
    print("[CamelGate] Initializing...")
    os_type = platform.system()
    print(f"[CamelGate] Detected OS: {os_type}")
    monitor_outbound()

if __name__ == "__main__":
    main()