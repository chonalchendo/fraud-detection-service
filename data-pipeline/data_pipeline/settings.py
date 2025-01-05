from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageOptions(BaseSettings):
    AWS_S3_LOCKING_PROVIDER: str = "dynamodb"
    DELTA_DYNAMO_TABLE_NAME: str = "delta_log"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str


storage_options = StorageOptions().dict()
