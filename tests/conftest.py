"""
Shared fixtures for build agent tests
"""
import subprocess
import pytest


@pytest.fixture(scope="session")
def docker_available():
    """Check Docker is available on the test machine"""
    result = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        pytest.skip("Docker not available")
    return True


@pytest.fixture(scope="session")
def built_images(docker_available):
    """Return list of expected built images"""
    return [
        "build-agent:base",
        "build-agent:python",
        "build-agent:node",
        "build-agent:java",
    ]


def run_in_container(image: str, command: str) -> subprocess.CompletedProcess:
    """Helper — run a command inside a container and return result"""
    return subprocess.run(
        ["docker", "run", "--rm", image, "sh", "-c", command],
        capture_output=True,
        text=True
    )
