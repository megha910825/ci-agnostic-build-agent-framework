# Getting Started

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Ansible | >= 2.15 | `pip install ansible-core==2.15.13` |
| Docker | >= 24.0 | [docs.docker.com](https://docs.docker.com/engine/install/) |
| Python | >= 3.10 | [python.org](https://python.org) |
| Molecule | >= 6.0 | `pip install molecule molecule-docker` |

---

## 1. Clone the Repository

```bash
git clone https://github.com/megha910825/ci-agnostic-build-agent-framework.git
cd ci-agnostic-build-agent-framework
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
## 2.  Install Ansible Collections

```bash
   ansible-galaxy collection install -r ansible/requirements.yml
```
## 3. Choose Your CI System
Edit ansible/roles/agent-setup/defaults/main.yml
```bash
   ci_system: github-actions   # github-actions | azure-pipelines | teamcity
   agent_version: "2.311.0"
   agent_token: ""             # set at runtime — never commit this

```
## 4. Build Docker Agent Images
```bash
   docker compose build
   docker images | grep build-agent

```
## 5. Run Molecule Tests
```bash
cd ansible/roles/agent-setup && molecule test
cd ../docker-install        && molecule test
cd ../agent-hardening       && molecule test
```
## 6. Provision a Real Agent Host
```bash
ansible-playbook ansible/playbook.yml \
  -i your-host-ip, \
  -e "ci_system=github-actions" \
  -e "agent_token=YOUR_TOKEN"
```

## 7. Verify Agent Health
```bash
python3 scripts/health-check.py --ci github-actions
```

