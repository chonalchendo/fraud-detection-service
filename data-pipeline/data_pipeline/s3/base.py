import os

import s3fs


def base_s3() -> s3fs.S3FileSystem:
    return s3fs.S3FileSystem(
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
        anon=False,
    )
