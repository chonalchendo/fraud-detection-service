from time import sleep

import polars as pl

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic


class TopicCreationError(Exception):
    pass


class StreamCreationError(Exception):
    pass


def create_stream(topic: str, servers: list[str]) -> None:
    producer, admin = _initialise_kafka(servers=servers)

    _create_kafka_topic(admin=admin, topic=topic)

    prod_data_path = "s3://fraud-detection-system/production/prod.parquet"
    print(f"Reading data from S3 path: {prod_data_path}")

    df = pl.read_parquet(prod_data_path)

    while True:
        for record in df.to_dicts():
            producer.send(topic=topic, value=record)
            print(f"SUCCESS - Sent record to Kafka topic {topic}")
            sleep(1)


def _create_kafka_topic(admin: KafkaAdminClient, topic: str) -> None:
    try:
        topic = NewTopic(name=topic, num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        print(f"SUCCESS - Created topic {topic}")
    except TopicCreationError as e:
        print(f"ERROR - Failed to create topic {topic} with error {e}")


def _initialise_kafka(servers: list[str]) -> tuple[KafkaProducer, KafkaAdminClient]:
    for i in range(20):
        try:
            producer = KafkaProducer(bootstrap_servers=servers)
            admin = KafkaAdminClient(bootstrap_servers=servers)
            print("SUCCESS - Connected to Kafka")
            break
        except StreamCreationError as e:
            print(
                f"Trying to instantiate admin and producer with bootstrap servers {servers} with error {e}"
            )
            sleep(10)
            pass

    return producer, admin


if __name__ == "__main__":
    TOPIC = "transactions"
    SERVERS = ["localhost:9092"]

    create_stream(topic=TOPIC, servers=SERVERS)
