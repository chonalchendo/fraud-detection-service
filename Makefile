.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build     Build Docker images"
	@echo "  up        Start Docker containers"
	@echo "  down      Stop Docker containers"


.PHONY: build
build:
	@echo "Building Docker images..."
	docker compose -f docker-compose.yml build

.PHONY: up
up:
	@echo "Starting Docker containers..."
	docker compose -f docker-compose.yml up -d --remove-orphans

.PHONY: down
down:
	@echo "Stopping Docker containers..."
	docker compose -f docker-compose.yml down
