FROM build-agent:base

LABEL maintainer="Megha Bansal <bansalmegha.259@gmail.com>"
LABEL description="CI-agnostic Node.js build agent"

USER root

# Install nodejs + npm directly from Ubuntu apt
# Corporate network blocks nodesource and nodejs.org
# Ubuntu 22.04 ships Node 12 — sufficient for portfolio demo
# In CI/production environments this builds with Node 20 via nodesource
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Verify node and npm
RUN node --version && npm --version

RUN npm install -g \
    typescript@4.9.5 \
    prettier@2.8.8 \
    --registry https://registry.npmjs.org \
    --strict-ssl=false

USER agent

# Verify tools
RUN node --version && npm --version && tsc --version && \
    prettier --version
