.PHONY: install test run lint format clean

# Installation
install:
	uv pip install -e .

# Development installation with test dependencies
install-dev:
	uv pip install -e ".[dev]"

# Run the application
run:
	uvicorn app.main:app --reload

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=term --cov-report=html

# Run formatter
format:
	black app tests main.py

# Run linter
lint:
	flake8 app tests main.py

# Clean build artifacts
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	rm -rf .eggs

# Help
help:
	@echo "make install      - Install the package"
	@echo "make install-dev  - Install the package with development dependencies"
	@echo "make run          - Run the application"
	@echo "make test         - Run tests"
	@echo "make test-cov     - Run tests with coverage"
	@echo "make format       - Format code"
	@echo "make lint         - Run linter"
	@echo "make clean        - Clean build artifacts" 