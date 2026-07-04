.PHONY: help install install-dev lint format test test-cov type-check clean run docker-build docker-up docker-down

PYTHON := python
PIP := pip
APP_DIR := app

help:
	@echo "Available commands:"
	@echo "  install        Install production dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo "  lint           Run Ruff linter"
	@echo "  format         Format code with Ruff and Black"
	@echo "  test           Run all tests"
	@echo "  test-cov       Run tests with coverage"
	@echo "  type-check     Run MyPy type checker"
	@echo "  quality        Run all quality checks (lint, format, type-check, test)"
	@echo "  clean          Clean generated files"
	@echo "  run            Run the application"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-up      Start Docker containers"
	@echo "  docker-down    Stop Docker containers"

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

lint:
	ruff check .

format:
	black .
	ruff format .

test:
	pytest $(APP_DIR)/tests

test-cov:
	pytest --cov=$(APP_DIR) --cov-report=html --cov-report=term

type-check:
	mypy $(APP_DIR)

quality: lint format type-check test

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

run:
	$(PYTHON) -m $(APP_DIR)

docker-build:
	docker build -t alphahunter-ai:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
