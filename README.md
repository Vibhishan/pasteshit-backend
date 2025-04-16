# PasteShit Backend

A simple pastebin-like API built with FastAPI and SQLite.

## Features

- Create text pastes
- Retrieve pastes by ID
- Delete pastes
- Optional expiration for pastes

## Project Structure

```
pasteshit-backend/
├── app/                 # Main application package
│   ├── __init__.py     # Package initialization
│   ├── main.py         # Application entry point
│   ├── api/            # API related code
│   │   ├── __init__.py
│   │   └── v1/         # API version 1
│   │       ├── __init__.py
│   │       ├── api.py  # API router configuration
│   │       ├── schemas.py  # Pydantic models
│   │       └── endpoints/  # API endpoints
│   │           ├── __init__.py
│   │           └── pastes.py
│   ├── core/           # Core functionality
│   │   ├── __init__.py
│   │   └── config.py   # Application settings
│   └── database/       # Database related code
│       ├── __init__.py
│       ├── connection.py  # Database connection
│       ├── models.py      # SQLAlchemy models
│       └── crud.py        # Database operations
├── tests/              # Test files
│   ├── __init__.py
│   ├── conftest.py     # Test configuration
│   └── api/            # API tests
│       └── v1/         # API v1 tests
│           ├── __init__.py
│           └── test_pastes.py
├── .env               # Environment variables
├── .env.example       # Example environment variables
├── .gitignore        # Git ignore file
├── Makefile          # Common commands
└── pyproject.toml    # Project dependencies
```

## Setup

1. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
# Install main dependencies
uv pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"
```

3. Run the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.

## Development Tools

The project includes several development tools:

- **Black**: Code formatting
- **Flake8**: Code linting
- **Pytest**: Testing framework
- **Pytest-cov**: Test coverage

Use the Makefile for common commands:

```bash
make install      # Install the package
make install-dev  # Install with development dependencies
make run         # Run the application
make test        # Run tests
make test-cov    # Run tests with coverage
make format      # Format code
make lint        # Run linter
make clean       # Clean build artifacts
```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Database configuration
DATABASE_URL=sqlite:///./pastebin.db

# Security configuration
SECRET_KEY=dev_secret_key_change_in_production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Application configuration
DEBUG=True
```

## Running Tests

To run tests:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=term --cov-report=html
```
