# Base: Debian 12 (Bookworm) matches Google Distroless runtime (gcr.io/distroless/*-debian12)
# This ensures binary compatibility between build and runtime environments.
FROM mcr.microsoft.com/devcontainers/base:debian-12

# Note: All tooling (uv, shellcheck) is now installed via Dev Container Features
# defined in devcontainer.json. This keeps the Dockerfile standard and minimal.
# Install CI and Ecosystem Tools via official images using multi-stage builds.
# This eliminates reliance on running Docker out of Docker inside the container for static analysis.
COPY --from=aquasec/trivy:latest /usr/local/bin/trivy /usr/local/bin/trivy
COPY --from=trufflesecurity/trufflehog:latest /usr/bin/trufflehog /usr/local/bin/trufflehog
COPY --from=hadolint/hadolint:latest-debian /bin/hadolint /usr/local/bin/hadolint
COPY --from=koalaman/shellcheck:stable /bin/shellcheck /usr/local/bin/shellcheck
# Py Ecosystem Tooling
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Use non-root user (enforced by Trivy AVD-DS-0002)
USER vscode
