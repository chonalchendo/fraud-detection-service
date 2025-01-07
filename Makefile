

# Publish packages commands

run-tests:
	@echo "Running tests"
	cd data-pipeline
	uv run pytest tests
	@echo "Tests ran successfully!"

publish-packages:
	@echo "Publishing packages to AWS CodeArtifact"
	cd data-pipeline
	uv build
	uv publish
	@echo "Packages published successfully!"


