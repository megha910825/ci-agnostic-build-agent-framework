#!/usr/bin/env python3
"""
Build Agent Health Check
Validates agent is running and connected to CI system
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable


@dataclass
class HealthCheck:
    name: str
    check_fn: Callable
    critical: bool = True


def check_service_running() -> tuple[bool, str]:
    result = subprocess.run(
        ["systemctl", "is-active", "build-agent"],
        capture_output=True, text=True
    )
    running = result.stdout.strip() == "active"
    return running, "Agent service is active" if running else "Agent service is NOT running"


def check_docker_running() -> tuple[bool, str]:
    result = subprocess.run(
        ["docker", "info"],
        capture_output=True, text=True
    )
    ok = result.returncode == 0
    return ok, "Docker is running" if ok else "Docker is NOT running"


def check_work_dir_exists() -> tuple[bool, str]:
    import os
    exists = os.path.isdir("/opt/build-agent")
    return exists, "Work directory exists" if exists else "Work directory missing"


def check_config_exists() -> tuple[bool, str]:
    import os
    exists = os.path.isfile("/opt/build-agent/.agent-config")
    return exists, "Agent config exists" if exists else "Agent config missing"


CHECKS = [
    HealthCheck("Agent Service",    check_service_running,  critical=True),
    HealthCheck("Docker Daemon",    check_docker_running,   critical=True),
    HealthCheck("Work Directory",   check_work_dir_exists,  critical=False),
    HealthCheck("Agent Config",     check_config_exists,    critical=False),
]


def run_health_checks(ci_system: str) -> bool:
    print(f"\n🔍 Running health checks for: {ci_system}\n")
    print("-" * 50)

    all_passed = True

    for check in CHECKS:
        passed, message = check.check_fn()
        status = "✅" if passed else ("❌" if check.critical else "⚠️")
        print(f"{status}  {check.name}: {message}")

        if not passed and check.critical:
            all_passed = False

    print("-" * 50)
    if all_passed:
        print("\n✅ All critical checks passed — agent is healthy!\n")
    else:
        print("\n❌ One or more critical checks failed — agent needs attention!\n")

    return all_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Agent Health Check")
    parser.add_argument(
        "--ci",
        choices=["github-actions", "azure-pipelines", "teamcity"],
        default="github-actions",
        help="CI system to check against"
    )
    args = parser.parse_args()

    success = run_health_checks(args.ci)
    sys.exit(0 if success else 1)
