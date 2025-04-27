import platform
import socket
import time
from datetime import datetime
from core_api.communication import report_to_core

AGENT_ID = "LongLegs-001"
SCAN_INTERVAL = 600  # Scan every 10 minutes (adjust as needed)

def log_alert(message, threat_type="Suspicious Activity"):
    timestamp = datetime.now().isoformat()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    payload = {
        "agent_id": AGENT_ID,
        "timestamp": timestamp,
        "hostname": hostname,
        "device_ip": ip_address,
        "threat_type": threat_type,
        "details": message,
        "status": "pending",
        "score": 2
    }

    report_to_core(payload)
    print(f"[LongLegs] {message}")

def perform_basic_checks():
    print("[LongLegs] Performing basic system integrity checks...")
    os_type = platform.system()

    if os_type == "Windows":
        # Example check: Detect elevated PowerShell sessions
        import psutil
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and "powershell.exe" in proc.info['name'].lower():
                log_alert("Detected active PowerShell session.")
    
    elif os_type == "Linux":
        # Example check: Detect unauthorized crontab entries (very basic)
        try:
            import subprocess
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout:
                entries = [line for line in result.stdout.splitlines() if line.strip() and not line.startswith("#")]
                if entries:
                    log_alert(f"Crontab entries detected: {len(entries)} entries.")
        except Exception as e:
            log_alert(f"Error checking crontab: {e}", threat_type="Agent Error")

    else:
        log_alert(f"Unsupported OS detected: {os_type}", threat_type="Agent Error")

def main():
    print("[LongLegs] Agent started.")
    while True:
        perform_basic_checks()
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
