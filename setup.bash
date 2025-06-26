#!/bin/bash

# Check if 'uv' is installed
if ! command -v uv &> /dev/null; then
    echo "[INFO] 'uv' not found. Install with: pip install uv"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    uv venv
fi

# Activate virtual environment
if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
else
    echo "[ERROR] Failed to create or find .venv virtual environment."
    exit 1
fi

# # Source .env file if it exists
# if [ -f .env ]; then
#     set -a
#     source .env
#     set +a
# fi

# Sync dependencies
uv sync

echo "[INFO] To install dependencies, run: uv sync"
echo "[INFO] To activate the virtual environment, run: source ./.venv/bin/activate"
echo "[INFO] Environment is set up. You can now run your agent or web server."
