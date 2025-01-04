kaggle-extract-data:
	@echo "Extracting data from Kaggle"
	uv run python -m data_pipeline.download
	@echo 'Removing files from local data directory'
	rm -rf data/
