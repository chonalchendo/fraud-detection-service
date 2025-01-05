"""
This script donwloads the dataset from kaggle, converts each .csv file to
.parquet, then uploads to s3 buckets.

The fraudTrain.csv file will be used to train, validate, and test the initial model.
The fraudTest.csv file will be used as production data, simulating real-time 
transaction data feeding to the trained model using Kafka.

Date: 2025-01-04
"""

from hashlib import sha256
from pathlib import Path

import kaggle
import polars as pl
import s3
from rich import print

from .constants import SENSITIVE_COLS


def extract_from_kaggle() -> None:
    """
    Main function to download the dataset from kaggle, convert to parquet,
    and upload to s3.
    """
    # download data from kaggle
    _download_data()

    orig_paths = Path("data").glob("*.csv")

    for path in orig_paths:
        _convert_to_parquet(path)

    # add customer id to both datasets
    train_df = pl.read_parquet("data/fraudTrain.parquet")
    test_df = pl.read_parquet("data/fraudTest.parquet")

    train_data, test_data = _generate_customer_id(
        train_df=train_df, test_df=test_df, sensitive_cols=SENSITIVE_COLS
    )

    train_data.write_parquet("data/fraudTrain.parquet")
    test_data.write_parquet("data/fraudTest.parquet")

    paths = [
        ("data/fraudTrain.parquet", "raw/training.parquet"),
        ("data/fraudTest.parquet", "production/prod.parquet"),
    ]

    BUCKET = "fraud-detection-system"

    for input, output in paths:
        s3.write(bucket=BUCKET, input=input, output=output)


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


def _generate_customer_id(
    train_df: pl.DataFrame, test_df: pl.DataFrame, sensitive_cols: list[str]
) -> tuple[pl.DataFrame, pl.DataFrame]:
    print("generating customer id")

    def __create_customer_id(row: dict) -> str:
        identifier = (
            f"{str(row['first']).lower().strip()}"
            f"{str(row['last']).lower().strip()}"
            f"{str(row['cc_num']).strip()}"
            f"{str(row['dob'])}"
        )
        # Create deterministic hash
        return f"CUST_{sha256(identifier.encode()).hexdigest()[:16]}"

    print("creating concatenating train and test data")
    full_data = pl.concat(
        [
            train_df.with_columns(pl.lit("train").alias("original_split")),
            test_df.with_columns(pl.lit("test").alias("original_split")),
        ]
    )

    print('mapping "create_customer_id" function to sensitive columns')
    processed_data = full_data.with_columns(
        pl.struct(sensitive_cols)
        .map_elements(lambda x: __create_customer_id(x), return_dtype=pl.String)
        .alias("customer_id")
    )

    # split data hack into train and test
    print("splitting data back into train and test")
    train_data = processed_data.filter(pl.col("original_split") == "train").drop(
        "original_split"
    )
    test_data = processed_data.filter(pl.col("original_split") == "test").drop(
        "original_split"
    )

    print(
        'asserting "train_data" and "test_data" have the same length as "train_df" and "test_df"'
    )
    assert len(train_df) == len(train_data)
    assert len(test_df) == len(test_data)

    return train_data, test_data


if __name__ == "__main__":
    extract_from_kaggle()
