#!/usr/bin/env bash
# DevOps Mastery Tracker — One-command setup for Mac
# Usage: chmod +x setup.sh && ./setup.sh

set -euo pipefail

echo "=== DevOps Mastery Tracker Setup ==="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 not found. Install from python.org or: brew install python"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_VERSION" -lt 9 ]; then
    echo "ERROR: Python 3.9+ required. Current: 3.$PYTHON_VERSION"
    exit 1
fi

echo "✓ Python 3.$PYTHON_VERSION found"

# Create virtualenv
if [ ! -d "tracker/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv tracker/.venv
fi
echo "✓ Virtual environment ready"

# Install deps
echo "Installing dependencies..."
tracker/.venv/bin/pip install --quiet --upgrade pip
tracker/.venv/bin/pip install --quiet -r tracker/requirements.txt
echo "✓ Dependencies installed"

# Launch
echo ""
echo "=== Launching DevOps Mastery Tracker ==="
echo "Opening at: http://localhost:8501"
echo "Press Ctrl+C to stop."
echo ""

tracker/.venv/bin/streamlit run tracker/app.py \
    --server.port 8501 \
    --server.headless false \
    --browser.gatherUsageStats false
