## **Backend Design Document: Pastebin Clone (FastAPI & SQLite)**

Version: 1.0  
Date: 2025-04-16  
Based on PRD: pastebin\_prd\_v1  
**1\. Introduction**

This document details the design and architecture for the backend service of the Pastebin Clone application. It adheres to the functional requirements specified in pastebin\_prd\_v1 and utilizes Python with the FastAPI framework and SQLite for database persistence. The focus is on creating a functional MVP suitable for a learning project, prioritizing clarity and simplicity over production-level optimizations like CI/CD or advanced scaling solutions.

**2\. Technology Stack**

* **Language:** Python (3.13+)  
* **Web Framework:** FastAPI  
* **Web Server (for development):** Uvicorn  
* **Database:** SQLite 3  
* **Data Validation:** Pydantic (integrated with FastAPI)  
* **Database Interaction:** Standard sqlite3 module or potentially SQLAlchemy Core (for more structured queries, optional) or aiosqlite (for async, optional). We'll assume standard sqlite3 for simplicity initially.  
* **Unique ID Generation:** nanoid Python library.  
* **Environment Management:** venv

**3\. Architecture Overview**

The backend will be a single, monolithic API service built with FastAPI.

* **Request Flow:** Incoming HTTP requests hit the Uvicorn server, which forwards them to the FastAPI application. FastAPI routes the request based on the path and method to the corresponding path operation function.  
* **Data Validation:** Pydantic models defined in the FastAPI path operations automatically parse and validate incoming request bodies and parameters.  
* **Business Logic:** Path operation functions contain the core logic, including generating unique IDs and interacting with the database.  
* **Database Interaction:** Logic functions execute SQL queries against the SQLite database file to create or retrieve paste records.  
* **Response Generation:** FastAPI automatically converts return values (or Pydantic models) into JSON HTTP responses, handling appropriate status codes and headers. FastAPI also automatically generates interactive API documentation (Swagger UI / ReDoc).

**4\. Database Design**

* **Database System:** SQLite  
* **Database File:** pastebin.db (located in the project root or a designated data directory)  
* **Table Schema:**  
  CREATE TABLE IF NOT EXISTS pastes (  
      id TEXT PRIMARY KEY NOT NULL,  \-- Unique, short identifier (e.g., from nanoid)  
      content TEXT NOT NULL,         \-- The text content of the paste  
      created\_at TIMESTAMP NOT NULL DEFAULT CURRENT\_TIMESTAMP \-- Auto-set creation time  
  );

* **Indexing:** The id column serves as the PRIMARY KEY, which automatically creates an index for efficient lookups.  
* **Notes:** SQLite is suitable for development and low-concurrency scenarios. It's simple as it's just a single file. For higher concurrency, a different database like PostgreSQL would be recommended in a production environment.

**5\. API Endpoint Design (FastAPI Implementation)**

We will implement the two core endpoints defined in the PRD.

**5.1. POST /api/v1/pastes \- Create Paste**

* **Purpose:** Receives text content, generates a unique ID, stores it, and returns the ID.  
* **FastAPI Decorator:** @app.post("/api/v1/pastes", response\_model=schemas.PasteResponse, status\_code=status.HTTP\_201\_CREATED)  
* **Request Body Model (Pydantic \- schemas.py):**  
  from pydantic import BaseModel, Field  
  import datetime

  class PasteCreate(BaseModel):  
      content: str \= Field(..., min\_length=1) \# Require non-empty content

* **Response Model (Pydantic \- schemas.py):**  
  class PasteResponse(BaseModel):  
      id: str

* **Path Operation Function (routers/pastes.py):**  
  from fastapi import APIRouter, HTTPException, Depends, status  
  from .. import schemas, crud, database \# Assuming project structure

  router \= APIRouter()

  @router.post("/api/v1/pastes", response\_model=schemas.PasteResponse, status\_code=status.HTTP\_201\_CREATED)  
  async def create\_paste(paste: schemas.PasteCreate, db: database.SessionLocal \= Depends(database.get\_db)):  
      \# 1\. Generate Unique ID (using crud.generate\_unique\_id \- see section 6\)  
      paste\_id \= crud.generate\_unique\_id(db) \# Pass db if checking uniqueness needed

      \# 2\. Create paste record in DB (using crud.create\_paste)  
      try:  
          created\_paste\_id \= crud.create\_paste(db=db, paste\_content=paste.content, paste\_id=paste\_id)  
          if not created\_paste\_id: \# Handle potential creation failure  
               raise HTTPException(status\_code=status.HTTP\_500\_INTERNAL\_SERVER\_ERROR, detail="Could not create paste")  
      except Exception as e: \# Catch specific DB errors if possible  
          \# Log the error e  
          raise HTTPException(status\_code=status.HTTP\_500\_INTERNAL\_SERVER\_ERROR, detail="Database error during paste creation")

      \# 3\. Return response  
      return schemas.PasteResponse(id=created\_paste\_id)

* **Dependencies:** crud.generate\_unique\_id, crud.create\_paste, database.get\_db.

**5.2. GET /api/v1/pastes/{paste\_id} \- Retrieve Paste**

* **Purpose:** Retrieves the content of a specific paste by its ID.  
* **FastAPI Decorator:** @app.get("/api/v1/pastes/{paste\_id}", response\_model=schemas.PasteDetailResponse)  
* **Path Parameter:** paste\_id: str  
* **Response Model (Pydantic \- schemas.py):**  
  class PasteDetailResponse(BaseModel):  
      id: str  
      content: str  
      created\_at: datetime.datetime \# Use datetime for type hinting

      class Config:  
          orm\_mode \= True \# If using SQLAlchemy ORM, otherwise manual mapping

* **Path Operation Function (routers/pastes.py):**  
  @router.get("/api/v1/pastes/{paste\_id}", response\_model=schemas.PasteDetailResponse)  
  async def get\_paste(paste\_id: str, db: database.SessionLocal \= Depends(database.get\_db)):  
      \# 1\. Fetch paste from DB (using crud.get\_paste)  
      db\_paste \= crud.get\_paste(db=db, paste\_id=paste\_id)

      \# 2\. Handle Not Found  
      if db\_paste is None:  
          raise HTTPException(status\_code=status.HTTP\_404\_NOT\_FOUND, detail="Paste not found")

      \# 3\. Return response (manual mapping shown if not using ORM mode)  
      return schemas.PasteDetailResponse(  
          id=db\_paste\[0\],      \# Assuming tuple result (id, content, created\_at)  
          content=db\_paste\[1\],  
          created\_at=db\_paste\[2\] \# May need parsing if stored as string  
      )  
      \# Or if using ORM mode and db\_paste is an ORM object: return db\_paste

* **Dependencies:** crud.get\_paste, database.get\_db.

**6\. Unique ID Generation (crud.py or utils.py)**

* **Library:** nanoid  
* **Implementation:**  
  import nanoid  
  \# Potentially add database access \`db\` if collision check is needed

  def generate\_unique\_id(db=None, size=8):  
      """Generates a unique nanoid. Optionally checks for collisions."""  
      \# Simple generation (sufficient for most cases with low volume)  
      new\_id \= nanoid.generate(size=size)  
      \# Optional: Add collision check loop if high volume expected  
      \# while crud.get\_paste(db, new\_id) is not None:  
      \#     new\_id \= nanoid.generate(size=size)  
      return new\_id

* **Size:** 8 characters provides \~4.3 trillion combinations (using default alphabet), sufficient for this project.

**7\. Error Handling**

* **Client Errors (4xx):**  
  * FastAPI automatically handles validation errors (e.g., missing content field) with 422 Unprocessable Entity.  
  * Use raise HTTPException(status\_code=404, detail="...") for "Not Found" errors.  
  * Use raise HTTPException(status\_code=400, detail="...") for other client-side errors (e.g., invalid parameters not caught by Pydantic).  
* **Server Errors (5xx):**  
  * Wrap database operations and other critical logic in try...except blocks.  
  * Catch specific exceptions (e.g., sqlite3.Error) if possible, log them.  
  * Raise HTTPException(status\_code=500, detail="Internal Server Error") to prevent leaking sensitive information. FastAPI can also have global exception handlers.

**8\. Configuration**

* For SQLite, the main configuration is the database file path. This can be hardcoded for simplicity or managed via environment variables using libraries like python-dotenv for better practice.  
  \# database.py  
  import os  
  from dotenv import load\_dotenv

  load\_dotenv() \# Load .env file

  DATABASE\_URL \= os.getenv("DATABASE\_URL", "sqlite:///./pastebin.db")  
  \# SQLALCHEMY\_DATABASE\_URL \= DATABASE\_URL \# If using SQLAlchemy  
  SQLITE\_DB\_FILE \= "./pastebin.db" \# If using direct sqlite3

  \# ... rest of database connection setup

**9\. Project Structure (Suggested)**

pastebin-backend/  
├── .venv/  
├── .env                 \# Store environment variables (e.g., DATABASE\_URL)  
├── .gitignore  
├── requirements.txt     \# Project dependencies  
├── main.py              \# FastAPI app creation and router inclusion  
├── database.py          \# Database connection setup (engine, session, get\_db)  
├── models.py            \# Database table models (SQLAlchemy ORM, if used)  
├── schemas.py           \# Pydantic models for request/response validation  
├── crud.py              \# Functions for database operations (Create, Read)  
└── routers/  
    ├── \_\_init\_\_.py  
    └── pastes.py        \# API router for paste-related endpoints

**10\. Setup and Running**

1. python \-m venv .venv  
2. source .venv/bin/activate (or .\\.venv\\Scripts\\activate on Windows)  
3. pip install \-r requirements.txt (containing fastapi, uvicorn\[standard\], nanoid, python-dotenv, optionally sqlalchemy, aiosqlite)  
4. **(First time)** Run a script or manually ensure the pastes table exists (e.g., via database.py on startup or a separate init script).  
5. uvicorn main:app \--reload (for development server)

**11\. "Cool Ideas" / Enhancements (For Learning)**

* **Raw Content Endpoint:** Add GET /raw/{paste\_id} that returns text/plain content directly using FastAPI's PlainTextResponse.  
* **Content Size Limit:** Add validation in schemas.PasteCreate or logic in the endpoint to limit the size of content (e.g., max\_length=100000).  
* **Async Database:** Explore using aiosqlite with async def endpoints for fully asynchronous handling (more complex setup).  
* **API Documentation Enhancement:** Add detailed descriptions, examples, and tags to FastAPI path operations and Pydantic models to enrich the auto-generated Swagger UI.  
* **Simple Rate Limiting:** Explore libraries like slowapi to add basic rate limiting per IP address.