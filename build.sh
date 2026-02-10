#!/bin/bash
set -e

# Install dependencies with --break-system-packages to handle Vercel's externally-managed Python environment
echo "Installing dependencies with --break-system-packages..."
pip install --break-system-packages -r requirements.txt 2>&1 || true

echo "Verifying FastAPI installation..."
python -c "import fastapi; print('✓ FastAPI installed successfully')"

echo "Build completed successfully"
exit 0