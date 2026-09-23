FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

# Keep the tool version explicit so a rebuilt development container provides
# the same uv CLI used to consume uv.lock.
COPY --from=ghcr.io/astral-sh/uv:0.12.13 /uv /uvx /usr/local/bin/

USER vscode
