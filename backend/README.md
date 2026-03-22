# Backend API - Real Estate Platform

## Technology Stack
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (with psycopg2-binary)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Structure
- `main.py`: Entry point and API routes.
- `database.py`: DB Connection configuration.
- `models.py`: SQLAlchemy models (User, Property, Appointment).
- `schemas.py`: Pydantic schemas for request/response validation.
- `crud.py`: Database operations.

## Setup Instructions
1. Create virtual environment: `python -m venv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` with DB Credentials.
4. Run server: `uvicorn main:app --reload`
