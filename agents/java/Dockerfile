FROM build-agent:base

LABEL maintainer="Megha Bansal <bansalmegha.259@gmail.com>"
LABEL description="CI-agnostic Java build agent"

USER root

# Install JDK 17
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    maven \
    && rm -rf /var/lib/apt/lists/*


# Set Java + Maven env vars
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV MAVEN_HOME=/opt/maven
ENV PATH="${MAVEN_HOME}/bin:${JAVA_HOME}/bin:${PATH}"

USER agent

# Verify tools
RUN java -version && mvn --version
