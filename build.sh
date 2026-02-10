#!/bin/bash
set -e

# Export environment variable to allow pip to break system packages
export PIP_BREAK_SYSTEM_PACKAGES=1

# Install dependencies with --break-system-packages to handle Vercel's externally-managed Python environment
echo "Installing dependencies from api/requirements.txt..."
pip install -r api/requirements.txt

echo "Verifying FastAPI installation..."
python -c "import fastapi; print('✓ FastAPI installed successfully')"

echo "Build completed successfully"
exit 0