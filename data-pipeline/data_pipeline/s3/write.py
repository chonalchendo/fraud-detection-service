from .base import base_s3


def write_bucket(bucket: str, input: str, output: str) -> None:
    print(f"Uploading {input} to s3://{bucket}/{output}")

    fs = base_s3()

    with fs.open(f"s3://{bucket}/{output}", "wb") as f:
        with open(input, "rb") as file:
            f.write(file.read())
