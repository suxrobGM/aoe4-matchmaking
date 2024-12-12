# Backend Service

The backend application is built using FastAPI and serves as the API for the AOE4 matchmaking system. It provides endpoints to add players to a queue, form matches, and predict match outcomes.

## Prerequisites

- [Python 3.12](https://www.python.org/downloads)
- [Poetry](https://python-poetry.org/docs) for dependency management.

## Installation

1. **Set up the Python environment (optional but recommended):**

   ```bash
   poetry config virtualenvs.in-project true
   ```

2. **Install dependencies:**

   ```bash
   poetry install
   ```

## Running the Backend

Use the following command to start the FastAPI server in development mode:

```bash
poetry run fastapi dev src/main.py
```

The API should be available at `http://localhost:8000/docs`.
