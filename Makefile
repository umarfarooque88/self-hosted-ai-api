# Self-Hosted AI API - Makefile
# Common development and deployment commands

.PHONY: help install run test clean docker-build docker-up docker-down

# Default target
help:
	@echo "Self-Hosted AI API - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "Development:"
	@echo "  make install     - Install dependencies"
	@echo "  make run         - Run the API server"
	@echo "  make dev         - Run with auto-reload"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linter"
	@echo "  make clean       - Clean up temporary files"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    - Build Docker images"
	@echo "  make docker-up       - Start Docker containers"
	@echo "  make docker-down     - Stop Docker containers"
	@echo "  make docker-logs     - View container logs"
	@echo ""
	@echo "Ollama:"
	@echo "  make ollama-serve    - Start Ollama server"
	@echo "  make ollama-pull     - Pull default model"
	@echo "  make ollama-list     - List installed models"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8

# Run the API server
run:
	python src/app.py

# Run in development mode with auto-reload
dev:
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	pytest tests/ -v --cov=src --cov-report=term-missing

# Run linter
lint:
	flake8 src/ tests/
	black --check src/ tests/

# Format code
format:
	black src/ tests/

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/
	rm -rf venv/ env/

# Docker commands
docker-build:
	docker-compose -f docker/docker-compose.yml build

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down

docker-logs:
	docker-compose -f docker/docker-compose.yml logs -f

docker-restart:
	docker-compose -f docker/docker-compose.yml restart

# Ollama commands
ollama-serve:
	ollama serve

ollama-pull:
	ollama pull qwen:1.8b

ollama-list:
	ollama list

# Full setup
setup: install ollama-pull
	@echo "Setup complete!"
	@echo "Copy .env.example to .env and configure"
