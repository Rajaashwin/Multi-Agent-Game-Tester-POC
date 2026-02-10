#!/bin/bash
set -e

echo "Verifying FastAPI installation..."
python -c "import fastapi; print('✓ FastAPI installed successfully')"

echo "Build completed successfully"
exit 0