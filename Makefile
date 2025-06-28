.DEFAULT-GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000
ENV_FILE ?= .dev.env

run:
	@uvicorn app.core.main:app --reload --host $(HOST) --port $(PORT) --env-file $(ENV_FILE)