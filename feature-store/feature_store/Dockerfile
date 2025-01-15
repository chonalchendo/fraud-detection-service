FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv pip install "feast[redis]"

COPY feature_store/config/feature_store.yaml feature_store.yaml

# Needed to reach online store within Docker network.
RUN sed -i 's/localhost:6379/redis:6379/g' feature_store.yaml
ENV FEAST_USAGE=False

CMD ["feast", "serve", "-h", "0.0.0.0"]
