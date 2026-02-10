#!/bin/bash
set -e

# Ensure pip reads our config and allows breaking system packages
export PIP_BREAK_SYSTEM_PACKAGES=1
export PIP_CONFIG_FILE="$PWD/.pip/pip.conf"

echo "Using pip config: $PIP_CONFIG_FILE"
echo "Installing dependencies with break-system-packages enabled..."
pip install -r requirements.txt

echo "Installation completed successfully"
exit 0
