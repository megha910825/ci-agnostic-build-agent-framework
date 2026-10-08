# CI System Integration Guide

## GitHub Actions

### 1. Register the runner
```bash
CI_SYSTEM=github-actions \
AGENT_TOKEN=your-token \
ansible-playbook ansible/playbook.yml -i your-host,
```

### 2. Use in your workflow
Copy ci-config/github-actions/build-agent-job.yml to your repo's .github/workflows/ and update the container.image to match your stack:

build-agent:python — Python projects
build-agent:node — Node.js projects
build-agent:java — Java/Maven projects

### Azure Pipelines
1. Register the agent
```bash
CI_SYSTEM=azure-pipelines \
AGENT_TOKEN=your-pat-token \
AZURE_DEVOPS_URL=https://dev.azure.com/your-org \
ansible-playbook ansible/playbook.yml -i your-host,
```
2. Use in your pipeline
Copy ci-config/azure-pipelines/build-agent-job.yml as your azure-pipelines.yml. Set pool.name to match the pool you registered the agent in (default: SelfHosted-AgentPool).

### Teamcity

1. Register the agent
```bash
CI_SYSTEM=teamcity \
TEAMCITY_SERVER_URL=http://your-server:8111 \
ansible-playbook ansible/playbook.yml -i your-host,
```
2. Approve the agent
After provisioning, go to: TeamCity UI → Administration → Build Agents → Unauthorized Agents and approve the new agent.

3. Reference the config
See ci-config/teamcity/build-agent-setup.xml for agent capability properties you can use in your build configuration requirements.

### Switching CI Systems
To move an agent from one CI system to another:
```bash
   # Re-run playbook with new ci_system value
ansible-playbook ansible/playbook.yml \
  -i your-host, \
  -e "ci_system=azure-pipelines" \
  -e "agent_token=new-token"

```
The agent config and systemd service are rewritten automatically. No manual cleanup needed.

