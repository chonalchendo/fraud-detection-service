import polars as pl

from ..settings import storage_options


def write_parquet(df: pl.DataFrame, bucket: str, table: str) -> None:
    print(f"Uploading {df} to s3://{bucket}/{table}")

    df.write_parquet(
        f"s3://{bucket}/{table}",
        storage_options=storage_options,
    )


def write_deltalake(df: pl.DataFrame, bucket: str, table: str):
    print(f"Uploading {df} to s3://{bucket}/{table}")
    df.write_delta(
        f"s3://{bucket}/{table}",
        storage_options=storage_options,
    )
