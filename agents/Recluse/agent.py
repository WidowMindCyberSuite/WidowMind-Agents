import psutil
import os
import json
import time
import platform
from datetime import datetime
from core_api.communication import report_to_core
import socket

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'recluse_config.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'recluse_alerts.log')
SCAN_INTERVAL = 5  # seconds between scans

DEFAULT_CONFIG = {
    "kill_targets": [
        "mimikatz.exe", "meterpreter.exe", "nc.exe", "netcat", "malware_sample.exe"
    ],
    "scan_interval": 5
}

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
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    payload = {
        "agent_id": "Recluse-001",
        "timestamp": timestamp,
        "hostname": hostname,
        "device_ip": ip_address,
        "threat_type": "Active Threat Neutralized",
        "details": message,
        "status": "confirmed",  # Recluse actively kills threats
        "score": 5
    }

    # Report to Core
    report_to_core(payload)

    # Local fallback logging
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} [Recluse ACTION] {message}\n")
    print(f"[Recluse] {message}")

def kill_suspicious_processes(kill_targets):
    print("[Recluse] Scanning for hostile processes...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and any(target.lower() in proc.info['name'].lower() for target in kill_targets):
                try:
                    proc.terminate()
                    log_alert(f"Terminated suspicious process: PID={proc.pid}, Name={proc.info['name']}")
                    time.sleep(1)
                    if proc.is_running():
                        proc.kill()
                        log_alert(f"Force-killed stubborn process: PID={proc.pid}, Name={proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    log_alert(f"Failed to terminate process: PID={proc.pid}, Name={proc.info['name']}, Reason={e}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def main():
    print("[Recluse] Initializing...")
    os_type = platform.system()
    print(f"[Recluse] Detected OS: {os_type}")

    config = load_config()
    interval = config.get('scan_interval', SCAN_INTERVAL)
    kill_targets = config.get('kill_targets', [])

    while True:
        kill_suspicious_processes(kill_targets)
        time.sleep(interval)

if __name__ == "__main__":
    main()
