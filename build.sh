#!/bin/bash
set -e

# Install dependencies with --break-system-packages to handle externally-managed Python
pip install --break-system-packages -r requirements.txt

echo "Dependencies installed successfully"
exit 0