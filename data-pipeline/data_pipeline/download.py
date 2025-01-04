"""
This script donwloads the dataset from kaggle, converts each .csv file to
.parquet, then uploads to s3 buckets.

The fraudTrain.csv file will be used to train, validate, and test the initial model.
The fraudTest.csv file will be used as production data, simulating real-time 
transaction data feeding to the trained model using Kafka.

Date: 2025-01-04
"""


import os
from pathlib import Path

import kaggle
import polars as pl
import s3fs
from rich import print


def extract_from_kaggle() -> None:
    _download_data()

    paths = Path("data").glob("*.csv")

    for path in paths:
        _convert_to_parquet(path)

    paths = [
        ("data/fraudTrain.parquet", "raw/training.parquet"),
        ("data/fraudTest.parquet", "production/prod.parquet"),
    ]

    BUCKET = "fraud-detection-system"

    for input, output in paths:
        _upload_to_s3(bucket=BUCKET, input=input, output=output)


def _download_data() -> None:
    kaggle.api.authenticate()

    print("creating path")
    Path("data").mkdir(exist_ok=True, parents=True)

    print("downloading dataset from kaggle")
    kaggle.api.dataset_download_files(
        dataset="kartik2112/fraud-detection", path="data", unzip=True
    )


def _convert_to_parquet(path: str | Path) -> None:
    print(f"converting {path} to parquet")

    output = str(path).replace(".csv", ".parquet")
    pl.read_csv(path).write_parquet(file=output)


def _upload_to_s3(bucket: str, input: str, output: str) -> None:
    print(f"Uploading {input} to s3://{bucket}/{output}")

    fs = s3fs.S3FileSystem(
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
        anon=False,
    )
    # fs.put(input, output)
    with fs.open(f"s3://{bucket}/{output}", "wb") as f:
        with open(input, "rb") as file:
            f.write(file.read())


if __name__ == "__main__":
    extract_from_kaggle()
