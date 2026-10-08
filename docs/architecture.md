# Architecture

## Overview

The framework has three layers:
 ┌────────────────────────────────────────────────────────┐
 │ CI Systems │ │ GitHub Actions Azure Pipelines TeamCity │
 └───────────────────────┬────────────────────────────────┘
                         │ connects to
 ┌───────────────────────▼─────────────────────────────────┐
 │ Docker Build Agents   │ │ base ──► python / node / java │
 └───────────────────────┬─────────────────────────────────┘
                         │ provisioned by
  ┌──────────────────────▼────────────────────────────────┐
  │ Ansible Roles │ agent-setup docker-install hardening  │
  └───────────────────────────────────────────────────────┘

## Ansible Roles

| Role | Responsibility |
|------|---------------|
| `agent-setup` | Creates agent user, work directory, config, systemd service |
| `docker-install` | Installs Docker CE, adds agent user to docker group |
| `agent-hardening` | SSH hardening, fail2ban, UFW firewall, file permissions |

## Docker Images

| Image | Base | Extra Tools |
|-------|------|-------------|
| `build-agent:base` | Ubuntu 22.04 | git, curl, docker CLI, python3 |
| `build-agent:python` | base | pytest, black, flake8, mypy, bandit |
| `build-agent:node` | base | Node 20, npm, yarn |
| `build-agent:java` | base | JDK 17, Maven |

## Key Design Decisions

**Single variable drives CI system selection**
The entire framework switches behaviour via `ci_system: github-actions|azure-pipelines|teamcity`.
One Jinja2 template generates the correct config for each.

**Molecule tests every role**
Each role has a full Molecule test suite — create, converge, idempotence, verify, destroy.
Idempotence is enforced — running a role twice must produce `changed=0`.

**Non-root agent user**
All agents run as a dedicated `build-agent` system user, never root.
Docker socket access is group-scoped to that user only.

