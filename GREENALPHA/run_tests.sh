#!/bin/bash

# This script runs all tests for the GreenAlpha project.

# Exit immediately if a command exits with a non-zero status.
set -e

# Activate the virtual environment if it exists
if [ -d ".venv" ]; then
    echo "▶️ Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️ Virtual environment not found. Running tests with system Python."
fi

# Run the tests
echo "▶️ Running tests..."
python -m unittest discover -s GREENALPHA/tests -p "test_*.py"

echo "✅ All tests passed!"
