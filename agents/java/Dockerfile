FROM build-agent:base

LABEL maintainer="Megha Bansal <bansalmegha.259@gmail.com>"
LABEL description="CI-agnostic Java build agent"

USER root

# Install JDK 17
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Maven
ARG MAVEN_VERSION=3.9.6
RUN curl -fsSL \
    https://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz \
    | tar -xz -C /opt/ \
    && ln -s /opt/apache-maven-${MAVEN_VERSION} /opt/maven

# Set Java + Maven env vars
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV MAVEN_HOME=/opt/maven
ENV PATH="${MAVEN_HOME}/bin:${JAVA_HOME}/bin:${PATH}"

USER agent

# Verify tools
RUN java -version && mvn --version
