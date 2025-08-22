.PHONY: help install install-dev install-prod setup test lint format clean docker-build docker-up docker-down init-db create-admin

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  install-prod - Install production dependencies (minimal)"
	@echo "  setup        - Set up the project (copy .env, init db)"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting (flake8, mypy)"
	@echo "  format       - Format code (black, isort)"
	@echo "  clean        - Clean up temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-up    - Start with Docker Compose"
	@echo "  docker-down  - Stop Docker Compose"
	@echo "  init-db      - Initialize database"
	@echo "  create-admin - Create admin user"
	@echo "  start        - Start the bot and API"
	@echo "  start-bot    - Start only the bot"
	@echo "  start-api    - Start only the API"
	@echo "  start-rasa   - Start Rasa server"

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

install-prod:
	pip install -r requirements-prod.txt

# Setup project
setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please edit it with your configuration."; \
	else \
		echo ".env file already exists."; \
	fi
	mkdir -p data

# Testing
test:
	python -m pytest app/tests/ -v

test-cov:
	python -m pytest app/tests/ -v --cov=app --cov-report=html

# Code quality
lint:
	flake8 app/ main.py manage.py
	mypy app/ main.py manage.py

format:
	black app/ main.py manage.py
	isort app/ main.py manage.py

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

# Docker commands
docker-build:
	docker build -t test-bot .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Database management
init-db:
	python manage.py init-db

create-admin:
	python manage.py create-admin

# Application start commands
start:
	python main.py

start-bot:
	python manage.py bot

start-api:
	python manage.py api

start-rasa:
	python manage.py rasa

# Development workflow
dev-setup: setup install-dev
	pre-commit install
	@echo "Development environment ready!"

prod-setup: setup install-prod
	@echo "Production environment ready!"

# Quick commands for development
dev: format lint test
	@echo "Development checks passed!"
