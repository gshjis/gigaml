# Pomodoro FastAPI

Pomodoro FastAPI is a time management tool designed to help you work with the Pomodoro Technique. The application is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Features

- Task management with the Pomodoro Technique.
- User authentication and authorization.
- Real-time updates and notifications.
- Caching for improved performance.

## Project Structure

Here is an overview of the project structure:

```
.
├── .dockerignore
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── poetry.lock
├── pomodoro.db
├── pyproject.toml
├── README.md
├── requirements.txt
├── .git/
├── .github/
├── .mypy_cache/
├── .venv/
├── .vscode/
├── alembic/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   ├── main.py
│   │   ├── redis.py
│   │   ├── settings.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── ping.py
│   │   ├── tasks.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── category.py
│   │   ├── task.py
│   │   ├── user.py
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── repository.py
│   │   ├── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── task.py
│   ├── service/
│   │   ├── __init__.py
│   │   ├── task.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── database.py
├── config/
│   ├── linters/
│   │   ├── .flake8
│   │   ├── .isort.cfg
│   │   ├── .mypy.ini
│   │   ├── .pylintrc
├── tests/
│   ├── __init__.py
│   ├── fixtures.py
```

## Installation

To install the project dependencies, run:

```bash
poetry install
```

## Configuration

Create a `.env` file in the project root with the following content:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
```

## Running the Application

To run the application, use the following command:

```bash
uvicorn app.core.main:app --reload
```

## Dependencies

The project dependencies are specified in the `pyproject.toml` file. The main dependencies include:

- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Alembic
- Psycopg2-binary
- Redis
- Python-dotenv

## Development

To run the development server with auto-reloading, use:

```bash
poetry run uvicorn app.core.main:app --reload
```

## Linters and Formatters

The project uses the following linters and formatters:

- Flake8
- Pylint
- MyPy
- Black
- Isort
- Bandit

## Testing

To run the tests, use:

```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
