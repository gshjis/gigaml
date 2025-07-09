.DEFAULT_GOAL := help

# Переменные окружения
HOST ?= 0.0.0.0
PORT ?= 8000
ENV_FILE ?= .env
LOG_LEVEL ?= error
DB_SERVICE ?= db

# Помощь
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  run       - Start the development server"
	@echo "  migrate   - Create and apply database migrations (comment='Message')"
	@echo "  lint      - Run all linters"
	@echo "  format    - Auto-format code"
	@echo "  help      - Show this help"

# Запуск сервера
.PHONY: run
run:
	@uvicorn app.core.main:app --reload --host $(HOST) --port $(PORT) --env-file $(ENV_FILE)

.PHONY: run_container
run_container:
	@docker compose build
	@docker compose up -d

clean:
	@docker compose down --volumes --remove-orphans

.PHONY: apply_db
apply_db:
	@echo "DB created!"
	@alembic upgrade head