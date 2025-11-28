.PHONY: install install-dev lint format check test run clean sync help

# UV automatically creates and uses .venv
UV := uv

# Install dependencies (uv auto-creates .venv)
install:
	$(UV) sync

# Install with dev dependencies (uv auto-creates .venv)
install-dev:
	$(UV) sync --extra dev

# Sync dependencies (uv auto-creates .venv)
sync:
	$(UV) sync

# Linting (uv auto-activates .venv)
lint:
	$(UV) run ruff check .

# Format code (uv auto-activates .venv)
format:
	$(UV) run ruff format .

# Check and auto-fix (uv auto-activates .venv)
check:
	$(UV) run ruff check . --fix

# Run tests (uv auto-activates .venv)
test:
	$(UV) run pytest

# Run the application (uv auto-activates .venv)
run:
	$(UV) run streamlit run app.py

# Clean cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies (auto-creates .venv)"
	@echo "  make install-dev   - Install with dev tools (ruff, pytest)"
	@echo "  make sync          - Sync dependencies"
	@echo "  make lint          - Check code with ruff"
	@echo "  make format        - Format code with ruff"
	@echo "  make check         - Lint and auto-fix issues"
	@echo "  make test          - Run tests"
	@echo "  make run           - Run the Streamlit app"
	@echo "  make clean         - Clean cache and .venv"

