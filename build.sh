#!/bin/bash
# Cloudflare Pages Build Script for PR-Agent

set -euo pipefail

echo "Starting PR-Agent Cloudflare Pages Build Sequence..."

if [ "$CF_PAGES_BRANCH" = "main" ]; then
    echo "Running on 'main' branch. PR-Agent does not need to run on the default branch. Exiting gracefully."
    exit 0
fi

# Cloudflare Pages uses Python 3.13 by default in v3 but doesn't have uv installed.
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "Syncing dependencies..."
uv sync

if [ -z "$CF_PAGES_BRANCH" ]; then
    echo "Warning: CF_PAGES_BRANCH is not set. This script is intended to run in Cloudflare Pages."
    # We will try to run anyway, the python script might handle local usage or expect arguments.
else
    echo "Running PR-Agent for Branch: $CF_PAGES_BRANCH"
fi

# Execute the runner script
uv run run_pr_agent.py

echo "PR-Agent sequence completed successfully."
