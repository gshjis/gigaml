.DEFAULT_GOAL := help

# Переменные окружения
HOST ?= 0.0.0.0
PORT ?= 8000
ENV_FILE ?= .dev.env
LOG_LEVEL ?= error
DB_SERVICE ?= db  # Имя сервиса БД для Docker

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
	@uvicorn app.core.main:app --reload --host $(HOST) --port $(PORT) --env-file $(ENV_FILE) --log-level $(LOG_LEVEL)

# Миграции (используйте: make migrate comment="Your message")
.PHONY: migrate
migrate:
ifndef comment
	$(error Укажите сообщение для миграции: make migrate comment="Your message")
endif
	@alembic revision --autogenerate -m "$(comment)"
	@alembic upgrade head

# Линтеры
.PHONY: lint lint-flake8 lint-mypy lint-black lint-isort lint-pylint lint-bandit
lint: lint-flake8 lint-mypy lint-black lint-isort lint-pylint lint-bandit

lint-flake8:
	@flake8 app tests

lint-mypy:
	@mypy app tests

lint-black:
	@black --check app tests

lint-isort:
	@isort --check-only app tests

lint-pylint:
	@pylint app tests

lint-bandit:
	@bandit -r app

# Форматирование
.PHONY: format format-black format-isort
format: format-black format-isort

format-black:
	@black app tests

format-isort:
	@isort app tests

# Docker-версия миграций (если используете Docker)
.PHONY: docker-migrate
docker-migrate:
ifndef comment
	$(error Укажите сообщение: make docker-migrate comment="Message")
endif
	@docker-compose exec $(DB_SERVICE) alembic revision --autogenerate -m "$(comment)"
	@docker-compose exec $(DB_SERVICE) alembic upgrade head