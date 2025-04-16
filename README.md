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
├── config.py            # Configuration and environment variables
├── database.py          # Database connection and session management
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic models for request/response validation
├── crud.py              # Database operations
├── main.py              # Application entry point
├── routers/             # API routes
│   ├── __init__.py
│   └── pastes.py
├── tests/               # Test files
│   ├── __init__.py
│   └── test_pastes.py
└── pyproject.toml       # Project dependencies
```

## Setup

1. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
uv pip install -e .
```

3. Run the application:

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000.

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
DATABASE_URL=sqlite:///./pastebin.db
SECRET_KEY=your_secret_key
ALLOWED_ORIGINS=http://localhost:3000
DEBUG=True
```

## Running Tests

To run tests:

```bash
pytest
```
