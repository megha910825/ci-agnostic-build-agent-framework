#!/usr/bin/env bash
# =============================================================================
# Bootstrap script — sets up CI build agent from scratch
# Usage: curl -fsSL https://raw.githubusercontent.com/.../bootstrap.sh | bash
# =============================================================================
set -euo pipefail

# Colours
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()    { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()   { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Defaults
CI_SYSTEM="${CI_SYSTEM:-github-actions}"
AGENT_VERSION="${AGENT_VERSION:-2.311.0}"
WORK_DIR="${WORK_DIR:-/opt/build-agent}"

log "Starting build agent bootstrap..."
log "CI System  : ${CI_SYSTEM}"
log "Version    : ${AGENT_VERSION}"
log "Work Dir   : ${WORK_DIR}"

# Check OS
if [[ ! -f /etc/os-release ]]; then
    error "Cannot detect OS — only Linux is supported"
fi
source /etc/os-release
log "Detected OS: ${NAME} ${VERSION_ID}"

# Check Docker is installed
if ! command -v docker &>/dev/null; then
    warn "Docker not found — installing..."
    curl -fsSL https://get.docker.com | sh
    log "Docker installed ✅"
else
    log "Docker already installed ✅"
fi

# Check Python3 is installed
if ! command -v python3 &>/dev/null; then
    warn "Python3 not found — installing..."
    apt-get update && apt-get install -y python3 python3-pip
    log "Python3 installed ✅"
else
    log "Python3 already installed ✅"
fi

# Check Ansible is installed
if ! command -v ansible &>/dev/null; then
    warn "Ansible not found — installing..."
    pip3 install ansible
    log "Ansible installed ✅"
else
    log "Ansible already installed ✅"
fi

# Run Ansible playbook
log "Running Ansible provisioner..."
ansible-playbook ansible/playbook.yml \
    -i ansible/inventory/hosts.yml \
    -e "ci_system=${CI_SYSTEM}" \
    -e "agent_version=${AGENT_VERSION}" \
    --connection=local \
    -v

log ""
log "✅ Build agent bootstrap complete!"
log "Run: python3 scripts/health-check.py --ci ${CI_SYSTEM}"
