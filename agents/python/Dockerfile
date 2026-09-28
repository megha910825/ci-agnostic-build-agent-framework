FROM build-agent:base

LABEL maintainer="Megha Bansal <bansalmegha.259@gmail.com>"
LABEL description="CI-agnostic Python build agent"

USER root

# Install Python tooling
RUN apt-get update && apt-get install -y \
    python3-venv \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python build + test tools
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple/ \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --trusted-host pypi.python.org \
    pytest==8.0.0 \
    pytest-cov==4.1.0 \
    black==24.1.1 \
    flake8==7.0.0 \
    isort==5.13.2 \
    tox==4.12.0

# Copy Python agent requirements
COPY requirements.txt /home/agent/requirements-python.txt
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple/ \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --trusted-host pypi.python.org \
    -r /home/agent/requirements-python.txt

USER agent

# Verify tools are available
RUN python3 --version && pytest --version && black --version
