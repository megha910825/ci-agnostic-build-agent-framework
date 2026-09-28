"""
Tests that verify agent behaviour — user, permissions, capabilities
"""
import subprocess
import pytest


def run_in_container(image: str, command: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "run", "--rm", image, "sh", "-c", command],
        capture_output=True,
        text=True
    )


class TestAgentSecurity:
    def test_default_user_is_not_root(self):
        """Container should run as non-root by default"""
        result = run_in_container("build-agent:base", "whoami")
        assert result.returncode == 0
        assert result.stdout.strip() == "agent", \
            f"Expected 'agent' user, got: {result.stdout.strip()}"

    def test_agent_uid_nonzero(self):
        """agent user UID must not be 0 (root)"""
        result = run_in_container("build-agent:base", "id -u")
        assert result.returncode == 0
        assert int(result.stdout.strip()) > 0

    def test_workdir_is_home_agent(self):
        """Default working directory should be /home/agent"""
        result = run_in_container("build-agent:base", "pwd")
        assert result.returncode == 0
        assert result.stdout.strip() == "/home/agent"


class TestAgentCapabilities:
    def test_git_is_functional(self):
        """Agent should have a working git installation"""
        result = run_in_container(
            "build-agent:base",
            "git --version && git config --global init.defaultBranch main && git init /tmp/test-repo"
        )
        assert result.returncode == 0, \
            f"git init failed: {result.stderr}"

    def test_git_clone_skipped_on_corporate_network(self):
        """
        git clone from GitHub requires SSL cert trust.
        On corporate networks SSL is intercepted — this test
        is skipped locally but runs fine in GitHub Actions CI.
        """
        result = run_in_container(
            "build-agent:base",
            "git ls-remote https://github.com/octocat/Hello-World HEAD"
        )
        if result.returncode != 0 and "certificate" in result.stderr:
            pytest.skip(
                "Skipping git clone — corporate SSL interception detected. "
                "This test passes in GitHub Actions CI."
            )
        assert result.returncode == 0

    def test_python_can_run_script(self):
        """Python agent should execute a simple script"""
        result = run_in_container(
            "build-agent:python",
            "python3 -c \"print('hello from agent')\""
        )
        assert result.returncode == 0
        assert "hello from agent" in result.stdout

    def test_java_can_compile(self):
        """Java agent should compile and run a simple program"""
        result = run_in_container(
            "build-agent:java",
            "mkdir -p /tmp/test && "
            "echo 'public class T { public static void main(String[] a) "
            "{ System.out.println(\"ok\"); } }' > /tmp/test/T.java && "
            "javac /tmp/test/T.java && "
            "java -cp /tmp/test T"
        )
        assert result.returncode == 0
        assert "ok" in result.stdout

    def test_node_can_run_script(self):
        """Node agent should execute a simple JS script"""
        result = run_in_container(
            "build-agent:node",
            "node -e \"console.log('hello from node')\""
        )
        assert result.returncode == 0
        assert "hello from node" in result.stdout
