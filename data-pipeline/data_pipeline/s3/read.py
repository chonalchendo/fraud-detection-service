import polars as pl

from ..settings import storage_options


def read_parquet(bucket: str, file: str) -> pl.DataFrame:
    return pl.read_parquet(f"s3://{bucket}/{file}", storage_options=storage_options)
