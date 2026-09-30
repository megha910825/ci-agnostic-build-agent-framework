FROM build-agent:base

LABEL maintainer="Megha Bansal <bansalmegha.259@gmail.com>"
LABEL description="CI-agnostic Node.js build agent"

USER root

# Install nodejs + npm from Ubuntu apt
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Verify node and npm installed correctly
RUN node --version && npm --version

# Install tools — pinned to exact versions (DL3016)
RUN npm install -g \
    typescript@4.9.5 \
    prettier@2.8.8 \
    --registry https://registry.npmjs.org \
    --strict-ssl=false

USER 1000

RUN node --version && \
    npm --version && \
    tsc --version && \
    prettier --version

