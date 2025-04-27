# WidowMind Agents Deployment Guide

## 🧠 Introduction
Welcome to the deployment guide for WidowMind Agents. This document outlines the steps required to install, configure, and deploy the WidowMind Agents to client machines, ensuring secure communication with the WidowMind Core (Arachnocore).

---

## 🛠️ Prerequisites

- Python 3.8+
- `pip` package manager
- Valid Agent Certificates (client certificate and private key)
- Access to the WidowMind Core API endpoint (`https://arachnocore.yourdomain.com`)
- Agent API Key for authentication

---

## 📂 Repository Structure

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
├── certs/
│   ├── client_cert.pem
│   ├── client_key.pem
│   └── core_ca_cert.pem
├── requirements.txt
└── README.md / deployment_guide.md
```

---

## 🧩 Installation Steps

1. **Clone the Repository:**

```bash
git clone https://github.com/WidowMindCyberSuite/WidowMind-Agents.git
cd WidowMind-Agents
```

2. **Create and Activate Virtual Environment (Recommended):**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

3. **Install Required Packages:**

```bash
pip install -r requirements.txt
```

4. **Place Certificates:**
- Copy your `client_cert.pem`, `client_key.pem`, and `core_ca_cert.pem` files into the `certs/` directory.

5. **Configure Each Agent:**
- Each agent has a corresponding JSON configuration file.
- Modify thresholds, paths, or intervals as needed.

Example for CamelGate:
```json
{
  "browser": 104857600,
  "shell": 5242880,
  "other": 20971520
}
```

---

## 🚀 Running an Agent

From the project root, navigate to the desired agent folder and launch the agent:

```bash
cd agents/CamelGate
python agent.py
```

Or automate with supervisor/systemd for persistent background operation.

Example systemd service file (`camelgate.service`):
```ini
[Unit]
Description=WidowMind CamelGate Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/WidowMind-Agents/agents/CamelGate
ExecStart=/opt/WidowMind-Agents/venv/bin/python agent.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🔒 Security Notes

- All communication to WidowMind Core is encrypted via HTTPS with mutual TLS authentication.
- API keys must be kept secret and rotated periodically.
- Certificates should be stored securely and renewed annually.

---

## 🧹 Maintenance

- **Logs**: Each agent logs locally for offline analysis.
- **Updates**: Pull latest updates from the repository periodically.
- **Monitoring**: Implement optional check-in feature to monitor agent health.

---

## 📞 Support

For any issues, open a ticket at:
- [https://github.com/WidowMindCyberSuite/WidowMind-Agents/issues](https://github.com/WidowMindCyberSuite/WidowMind-Agents/issues)

Or contact the WidowMind Engineering Team.

---

> **WidowMind Philosophy:** _"Digital instincts. Autonomous defense. Evolving protection."_

🕸️ **Together, we weave an unbreakable digital defense.**