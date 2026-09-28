#!/usr/bin/env bash
# =============================================================================
# Cleanup script — tears down build agent and Docker images
# Usage: bash scripts/cleanup.sh [--images] [--all]
# =============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

REMOVE_IMAGES=false
REMOVE_ALL=false

# Parse args
for arg in "$@"; do
    case $arg in
        --images) REMOVE_IMAGES=true ;;
        --all)    REMOVE_ALL=true ;;
    esac
done

log "Starting cleanup..."

# Stop agent service if running
if systemctl is-active --quiet build-agent 2>/dev/null; then
    log "Stopping build-agent service..."
    systemctl stop build-agent
    systemctl disable build-agent
    log "Agent service stopped ✅"
else
    warn "build-agent service not running — skipping"
fi

# Remove agent work directory
if [[ -d /opt/build-agent ]]; then
    log "Removing agent work directory..."
    rm -rf /opt/build-agent
    log "Work directory removed ✅"
fi

# Remove Docker images if requested
if [[ "$REMOVE_IMAGES" == true ]] || [[ "$REMOVE_ALL" == true ]]; then
    log "Removing build-agent Docker images..."
    docker rmi build-agent:base   2>/dev/null && log "Removed build-agent:base ✅"   || warn "build-agent:base not found"
    docker rmi build-agent:python 2>/dev/null && log "Removed build-agent:python ✅" || warn "build-agent:python not found"
    docker rmi build-agent:node   2>/dev/null && log "Removed build-agent:node ✅"   || warn "build-agent:node not found"
    docker rmi build-agent:java   2>/dev/null && log "Removed build-agent:java ✅"   || warn "build-agent:java not found"
fi

# Full cleanup — remove Docker system too
if [[ "$REMOVE_ALL" == true ]]; then
    warn "Running full Docker system prune..."
    docker system prune -f
    log "Docker system pruned ✅"
fi

log ""
log "✅ Cleanup complete!"

