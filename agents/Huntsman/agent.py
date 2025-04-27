import os
import json
import time
import platform
import subprocess
from datetime import datetime
from core_api.communication import report_to_core

try:
    import winreg
except ImportError:
    winreg = None  # Not available on Linux

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'trapdoor_config.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'trapdoor_alerts.log')
SCAN_INTERVAL = 600  # 10 minutes by default

DEFAULT_CONFIG = {
    "check_registry": True,
    "check_scheduled_tasks": True,
    "check_crontab": True,
    "check_systemd": True,
    "scan_interval": 600
}

AGENT_ID = "Trapdoor-001"

WINDOWS_REGISTRY_RUN_KEYS = [
    r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
    r"Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce"
]

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_CONFIG

def log_alert(message, threat_type="Persistence Mechanism Detected", score=3):
    timestamp = datetime.now().isoformat()
    hostname = platform.node()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "0.0.0.0"

    payload = {
        "agent_id": AGENT_ID,
        "timestamp": timestamp,
        "hostname": hostname,
        "device_ip": ip_address,
        "threat_type": threat_type,
        "details": message,
        "status": "pending",
        "score": score
    }

    report_to_core(payload)

    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} [Trapdoor ALERT] {message}\n")
    print(f"[Trapdoor] {message}")

def check_windows_registry():
    if not winreg:
        return

    print("[Trapdoor] Scanning Windows registry Run keys...")
    for key_path in WINDOWS_REGISTRY_RUN_KEYS:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
            i = 0
            while True:
                try:
                    value = winreg.EnumValue(key, i)
                    log_alert(f"Registry persistence detected: {value[0]} = {value[1]}")
                    i += 1
                except OSError:
                    break
        except FileNotFoundError:
            continue

def check_windows_scheduled_tasks():
    print("[Trapdoor] Checking Windows scheduled tasks...")
    try:
        result = subprocess.run(["schtasks"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            lines = result.stdout.splitlines()
            for line in lines:
                if "/" not in line and "TaskName" not in line:
                    log_alert(f"Scheduled Task found: {line.strip()}")
    except Exception as e:
        log_alert(f"Error checking scheduled tasks: {e}", threat_type="Agent Error", score=1)

def check_linux_crontab():
    print("[Trapdoor] Checking Linux crontab entries...")
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.splitlines():
                if line.strip() and not line.startswith("#"):
                    log_alert(f"Crontab entry detected: {line.strip()}")
    except Exception as e:
        log_alert(f"Error reading crontab: {e}", threat_type="Agent Error", score=1)

def check_linux_systemd():
    print("[Trapdoor] Checking Linux systemd services...")
    try:
        result = subprocess.run(["systemctl", "list-unit-files"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.splitlines():
                if line.endswith("enabled"):
                    log_alert(f"Enabled systemd service: {line.strip()}")
    except Exception as e:
        log_alert(f"Error reading systemd services: {e}", threat_type="Agent Error", score=1)

def main():
    print("[Trapdoor] Initializing...")
    os_type = platform.system()
    print(f"[Trapdoor] Detected OS: {os_type}")

    config = load_config()
    interval = config.get('scan_interval', SCAN_INTERVAL)

    while True:
        if os_type == "Windows":
            if config.get("check_registry", True):
                check_windows_registry()
            if config.get("check_scheduled_tasks", True):
                check_windows_scheduled_tasks()

        elif os_type == "Linux":
            if config.get("check_crontab", True):
                check_linux_crontab()
            if config.get("check_systemd", True):
                check_linux_systemd()

        time.sleep(interval)

if __name__ == "__main__":
    main()
