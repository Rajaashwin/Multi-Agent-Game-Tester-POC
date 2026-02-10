#!/bin/bash
set -e

# Set pip configuration to allow breaking system packages
export PIP_BREAK_SYSTEM_PACKAGES=1

echo "Installing dependencies with break-system-packages enabled..."
pip install -r requirements.txt

echo "Installation completed successfully"
exit 0
