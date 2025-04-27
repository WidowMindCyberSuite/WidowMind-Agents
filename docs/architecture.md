# WidowMind Agents Architecture Document

## 🧠 Overview
WidowMind Agents are lightweight autonomous cybersecurity monitors deployed on client machines. Their mission is to gather threat intelligence and system telemetry, report findings securely to the WidowMind Core (Arachnocore), and optionally perform active defensive actions.

Each agent specializes in a specific aspect of threat detection, creating a "swarm intelligence" architecture.

---

## 🕸️ Components

| Module         | Description                                                                          |
|----------------|--------------------------------------------------------------------------------------|
| **CamelGate**  | Monitors outbound traffic for data exfiltration and abnormal transmission behavior. |
| **Huntsman**   | Scans for suspicious processes and anomalies in critical file paths.                |
| **Recluse**    | Actively neutralizes suspicious processes (threat termination/killing).             |
| **LongLegs**   | Detects system-level anomalies, such as unexpected elevated sessions or crontabs.   |
| **SunSpider**  | Monitors public IP exposure and DNS anomalies, checking for suspicious IPs.         |
| **Trapdoor**   | Detects persistence mechanisms (e.g., startup registry keys, crontabs, services).   |

---

## 🔗 Communication Flow

- **Agents → Core** (Primary Communication)
  - Agents package threat data into structured JSON payloads.
  - Secure HTTPS with **mutual TLS (mTLS)** ensures both endpoint and server authentication.
  - Payloads POSTed to Arachnocore at `/api/report` endpoint.

- **Core → Agents** (Optional Polling)
  - Agents may periodically poll `/api/check_in/<agent_id>` for tasks or configuration updates.

### Payload Example
```json
{
  "agent_id": "CamelGate-001",
  "timestamp": "2025-04-27T10:35:21Z",
  "hostname": "host-machine",
  "device_ip": "192.168.1.45",
  "threat_type": "High Outbound Traffic",
  "details": "Detected excessive data sent to 45.77.23.2",
  "status": "pending",
  "score": 4
}
```

---

## 🛡️ Security

- **Authentication**:
  - API Key header (`Authorization: Bearer <key>`) required.
  - Client must present trusted certificate (mTLS mutual authentication).

- **Encryption**:
  - All communication occurs over HTTPS (TLS 1.2+).

- **Certificate Validation**:
  - Agents validate Arachnocore server's CA.
  - Core validates each agent's presented certificate against trusted fingerprints.

---

## 🧬 Agent Lifecycles

1. **Initialize**:
   - Load configuration JSON.
   - Validate environment (OS, dependencies).

2. **Scan/Monitor**:
   - Passive monitoring (e.g., CamelGate, LongLegs).
   - Active scanning (e.g., Huntsman, Trapdoor).
   - Active response (e.g., Recluse neutralizes threats).

3. **Report**:
   - Immediately send detected events to Core.
   - Retry logic if reporting fails.

4. **(Optional) Check-In**:
   - Request new tasks from Core server.

5. **Sleep/Wait**:
   - Respect scan intervals to minimize system impact.

---

## 📜 Configuration Management

- Each agent has an independent JSON configuration file.
- Settings like scan intervals, process thresholds, detection toggles are agent-specific.
- Future enhancement: Remote configuration updates via Arachnocore.

---

## 🛠️ Deployment Structure

```
WidowMind-Agents/
├── agents/
│   ├── CamelGate/agent.py
│   ├── Huntsman/agent.py
│   ├── Recluse/agent.py
│   ├── LongLegs/agent.py
│   ├── SunSpider/agent.py
│   └── Trapdoor/agent.py
├── core_api/communication.py
├── certs/ (for agent certificates)
├── requirements.txt
└── README.md / architecture.md
```

---

## 🚀 Future Enhancements

- Dynamic agent updates
- Real reputation checks for IPs (AbuseIPDB, OTX integration)
- Decentralized fallback reporting
- Lightweight machine learning anomaly detection
- Native system hooks for faster persistence detection

---

> **WidowMind Philosophy:** _"Digital instincts. Autonomous defense. Evolving protection."_

🧬 **WidowMind Core + WidowMind Agents = Adaptive Cybersecurity Swarm Intelligence**.