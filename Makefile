.DEFAULT-GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

run:
	@echo "Server started"
	uvicorn main:app --reload --host $(HOST) --port $(PORT)