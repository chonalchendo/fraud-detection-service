# Kafka Producer

A Kafka producer is an application that writes messages (data) to a Kafka cluster. Is this example, the Kafka cluster is run locally
using Docker Compose and the messages are send to a topic called `raw_transactions`.

The overall architecture is that the producer will receive raw data (as data would be receieved in a production setting), send to a
Kafka topic, then the `feature-transformer` service will consume each message, transform the data, and write as a new topic called
`processed-transactions`. This new topic will then be consumed by the inference service which will make predictions on the data in
real-time, and to our offline storage for model training.

This archecture means we have an aligned data pipeline for training and inference.

## Steps to running this pipeline

1. Install Docker and Docker Compose
2. Install uv package mananger
3. Run make build
4. Run make up
5. Run make down
