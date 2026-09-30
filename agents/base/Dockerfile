FROM ubuntu:22.04

LABEL maintainer="Megha Bansal <bansalmegha.259@gmail.com>"
LABEL description="CI-agnostic base build agent"

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set shell to explicitly use bash with pipefail
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install base dependencies
RUN apt-get update && apt-get install -y --no-install-recommends\
    curl \
    git \
    wget \
    unzip \
    jq \
    ca-certificates \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (not daemon — uses host socket)
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
    https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*


RUN groupadd -f docker && \
    useradd -m -s /bin/bash -G docker agent


# Set working directory
WORKDIR /home/agent

# Copy base requirements
COPY requirements.txt .
# Install with SSL verification disabled for corporate network
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple/ \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --trusted-host pypi.python.org \
    -r requirements.txt

USER agent
