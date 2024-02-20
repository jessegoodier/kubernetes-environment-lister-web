# syntax=docker/dockerfile:1.0.0-experimental
# jgoodier/markdown2-kubectl
# A Docker image for markdown2 and kubectl

FROM alpine/k8s:1.29.1

# Update package lists and install required packages
# Install markdown2 using pip
RUN apk update \
    && apk add --no-cache pipx \
    && rm -rf ~/.cache/* /usr/local/share/man /tmp/* \
    && addgroup -g 1001 environment-lister \
    && adduser -G environment-lister -u 1001 environment-lister -D
USER 1001
RUN pipx install markdown2
ENV PATH="$PATH:/home/environment-lister/.local/bin"
