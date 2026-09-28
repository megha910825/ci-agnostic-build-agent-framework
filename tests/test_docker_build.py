"""
Tests that verify Docker images exist and are built correctly
"""
import subprocess
import pytest


def image_exists(image_name: str) -> bool:
    """Check if a Docker image exists locally"""
    result = subprocess.run(
        ["docker", "image", "inspect", image_name],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


class TestImagesExist:
    def test_base_image_exists(self):
        assert image_exists("build-agent:base"), \
            "build-agent:base image not found — run: docker compose build"

    def test_python_image_exists(self):
        assert image_exists("build-agent:python"), \
            "build-agent:python image not found — run: docker compose build"

    def test_node_image_exists(self):
        assert image_exists("build-agent:node"), \
            "build-agent:node image not found — run: docker compose build"

    def test_java_image_exists(self):
        assert image_exists("build-agent:java"), \
            "build-agent:java image not found — run: docker compose build"


class TestBaseAgent:
    def test_git_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:base", "git", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "git version" in result.stdout

    def test_python3_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:base", "python3", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0

    def test_docker_cli_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:base", "docker", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "Docker version" in result.stdout

    def test_agent_user_is_nonroot(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:base",
             "sh", "-c", "id -u agent"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert int(result.stdout.strip()) > 0, "agent user should not be root"


class TestPythonAgent:
    def test_pytest_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:python", "pytest", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "pytest" in result.stdout

    def test_black_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:python", "black", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0

    def test_flake8_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:python", "flake8", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0


class TestJavaAgent:
    def test_java_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:java", "java", "-version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0

    def test_maven_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:java", "mvn", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "Apache Maven" in result.stdout


class TestNodeAgent:
    def test_node_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:node", "node", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0

    def test_npm_installed(self):
        result = subprocess.run(
            ["docker", "run", "--rm", "build-agent:node", "npm", "--version"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
