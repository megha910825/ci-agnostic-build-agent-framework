FROM build-agent:base

LABEL maintainer="Megha Bansal <bansalmegha.259@gmail.com>"
LABEL description="CI-agnostic Node.js build agent"

USER root

# Install Node.js 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Yarn
RUN npm install -g yarn

# Install common Node build tools globally
RUN npm install -g \
    typescript \
    eslint \
    prettier \
    jest \
    @angular/cli

USER agent

# Verify tools
RUN node --version && npm --version && yarn --version
