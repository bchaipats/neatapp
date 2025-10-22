# Neatapp v2

A modular, extensible, and maintainable rewrite of Neatapp.

## Project Purpose

Neatapp v2 is a demonstration API for managing restaurant data, rebuilt to be maintainable and extensible using modern Python best practices. It features a modular, well-separated architecture suitable for scalable projects.

## High-level Architecture

- **FastAPI** is used for the web API framework.
- **SQLAlchemy** provides ORM functionality for managing the database.
- **Pydantic** is used for data validation and settings/configuration.
- The codebase is organized into logical modules/packages for clear separation of concerns.

### Key Directories/Modules
- `main.py`           : Application entry point, FastAPI app and router registration
- `config.py`         : Pydantic-based settings (environment, DB URL, debug, etc.)
- `db/`               : Database engine/session setup, session dependency
- `models/`           : ORM models (e.g. `Restaurant` in `restaurant.py`)
- `schemas/`          : Pydantic schemas for input/output validation & serialization
- `crud/`             : CRUD operations (select/insert/update/delete) for each entity
- `api/`              : API routers/endpoints organized per entity
- `services/`         : Business logic/services layer for core operations (extension point)
- `utils/`            : Utilities and helpers for use across the codebase

---

## Quickstart

1. **Install requirements** (you should have Python 3.10+ and poetry):
   ```bash
   poetry install
   ```
2. **Create the database:**
   ```bash
   poetry run python -c 'from neatapp.neatappv2.db.session import Base, engine; Base.metadata.create_all(bind=engine)'
   ```
3. **Run the server:**
   ```bash
   poetry run uvicorn neatapp.neatappv2.main:app --reload
   ```
4. **Visit the docs:**
   Go to [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Example Usage

- **List all restaurants:**
  ```http
  GET /restaurants/
  ```
- **Get a restaurant by ID:**
  ```http
  GET /restaurants/1
  ```
- **Create a new restaurant:**
  ```http
  POST /restaurants/
  Content-Type: application/json
  {
    "name": "Pizza Place",
    "description": "Great Italian pizza."
  }
  ```

---

## Technology Stack
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn (for development)

---

## Core Logic Location
- **Database Models**: `models/` (e.g., `restaurant.py`)
- **CRUD Operations**: `crud/` (e.g., `restaurant.py`)
- **Pydantic Schemas**: `schemas/`
- **API Endpoints**: `api/`
- **DB Handling**: `db/session.py`

---

## Extensibility & Adding New Features

To add a new resource/entity (e.g., `MenuItem`):
1. **Model**: Define a new SQLAlchemy model in `models/menu_item.py`.
2. **Schema**: Create `schemas/menu_item.py` with Pydantic schemas for serialization/validation.
3. **CRUD**: Add CRUD logic in `crud/menu_item.py`.
4. **API**: Add routes in `api/menu_item.py` using FastAPI's router.
5. **Service (optional)**: Add service/business logic in `services/menu_item_service.py` as needed.
6. **Register**: Include the router in `main.py`.

This modular organization keeps business logic, data validation, and API exposure cleanly separated and maintainable.

---

## Summary of Package Structure

- `main.py`           : Application entry point
- `config.py`         : Configuration and settings
- `db/`               : Database connection/session setup
- `models/`           : ORM models
- `schemas/`          : Pydantic/data validation schemas
- `crud/`             : CRUD logic
- `api/`              : API route definitions
- `services/`         : Core business logic
- `utils/`            : Utilities and helpers