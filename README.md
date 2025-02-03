# Test-Project for Cybernet


## Prerequisites

- Python 3.11 or higher
- PostgreSQL
- pip

## Installation and Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**
   - Create a PostgreSQL database named `test_cybernet`.


3. **Run Database Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start the Application**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI documentation at `http://localhost:8000/docs`
- ReDoc documentation at `http://localhost:8000/redoc`

## Environment Variables

Create a `.env` file in the root directory with the variables from `.env.example`

## Development

To make database migrations after model changes:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```
