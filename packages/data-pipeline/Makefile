kaggle-extract-data:
	@echo "Extracting data from Kaggle"
	uv run python -m data_pipeline.download
	@echo 'Removing files from local data directory'
	rm -rf data/

run-tests:
	@echo "Running tests"
	uv run pytest tests
	@echo "Tests ran successfully!"

publish-packages:
	@echo "Publishing packages to AWS CodeArtifact"
	uv build
	uv publish
	@echo "Packages published successfully!"


