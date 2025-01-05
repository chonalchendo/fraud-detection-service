import polars as pl

from .base import base_s3


def read_bucket(bucket: str, file: str) -> pl.DataFrame:
    fs = base_s3()

    with fs.open(f"s3://{bucket}/{file}", "rb") as f:
        return pl.read_parquet(f)
