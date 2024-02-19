# syntax=docker/dockerfile:1.0.0-experimental
# jgoodier/markdown2-kubectl
# A Docker image for markdown2 and kubectl

FROM alpine/k8s:1.29.1

# Update package lists and install required packages
RUN apk update && \
    apk add --no-cache pipx
# Install markdown2 using pip
RUN pipx install markdown2
RUN cp /root/.local/bin/markdown2 /usr/local/bin/markdown2