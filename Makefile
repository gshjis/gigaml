.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000
ENV_FILE ?= .dev.env
LOG_LEVEL ?= error

.PHONY: help run migrate

help:
	@echo "Available targets:"
	@echo "  run     - Start the development server"
	@echo "  migrate - Create and apply database migrations"
	@echo "  help    - Show this help message"

run:
	@uvicorn app.core.main:app --reload --host $(HOST) --port $(PORT) --env-file $(ENV_FILE) --log-level $(LOG_LEVEL)

migrate:
	@alembic revision --autogenerate -m "$(comment)"
	@alembic upgrade head