#!/bin/bash
set -e

echo "🚀 Setting up Fitness AI Advisor with UV and Ruff"
echo "=================================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ UV is installed"

# UV automatically creates .venv and installs dependencies
echo "📦 Installing dependencies (uv auto-creates .venv)..."
uv sync --extra dev

echo "✅ Dependencies installed in .venv"

# Format code
echo "🔧 Formatting code with ruff..."
uv run ruff format .

# Check code
echo "🔍 Checking code with ruff..."
uv run ruff check . --fix

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 UV automatically manages your virtual environment!"
echo "   No need to manually activate - just use 'uv run' or 'make' commands"
echo ""
echo "Useful commands:"
echo "  make run           - Run the application"
echo "  make lint          - Check code quality"
echo "  make format        - Format code"
echo "  make check         - Lint and auto-fix"
echo "  make install-dev   - Reinstall with dev tools"
echo ""
echo "Or run directly with UV:"
echo "  uv run streamlit run app.py"
echo "  uv run python script.py"

