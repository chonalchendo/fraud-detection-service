.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build     Build Docker images"
	@echo "  up        Start Docker containers"
	@echo "  down      Stop Docker containers"


# Load environment variables from .env file
ifeq (,$(wildcard .env))
$(error .env file not found. Please create one.)
endif
include .env
export $(shell sed 's/=.*//' .env)


# AWS commands

.PHONY: export-token
export-token:
	@echo "Generating AWS CodeArtifact token..."
	export AWS_CODEARTIFACT_TOKEN=$$(aws codeartifact get-authorization-token \
		--domain $(AWS_DOMAIN) \
		--domain-owner $(AWS_ACCOUNT_ID) \
		--query authorizationToken \
		--output text) && \
		echo "EXPORTED AWS_CODEARTIFACT_TOKEN: $$AWS_CODEARTIFACT_TOKEN"


# Docker commands

.PHONY: build
build:
	@echo "Starting Docker build..."
	@docker compose -f docker-compose.yml build --build-arg AWS_CODEARTIFACT_TOKEN=$$(aws codeartifact get-authorization-token \
		--domain $(AWS_DOMAIN) \
		--domain-owner $(AWS_ACCOUNT_ID) \
		--query authorizationToken \
		--output text)

.PHONY: up
up:
	@echo "Starting Docker containers..."
	docker compose -f docker-compose.yml up -d --remove-orphans

.PHONY: down
down:
	@echo "Stopping Docker containers..."
	docker compose -f docker-compose.yml down

