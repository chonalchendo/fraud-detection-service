FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    make \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip ./aws

# Set environment variables for AWS credentials
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_REGION
ARG AWS_ACCOUNT_ID
ARG AWS_DOMAIN
ARG AWS_CODEARTIFACT_REPOSITORY
ARG AWS_CODEARTIFACT_TOKEN

RUN echo "AWS CODEARTIFACT TOKEN: $AWS_CODEARTIFACT_TOKEN"


WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Copy the project's configuration files
COPY pyproject.toml uv.lock /app/

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY transformer/ /app/transformer/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev 


# Install package
RUN uv pip install data-pipeline==0.2.0 --extra-index-url "https://aws:${AWS_CODEARTIFACT_TOKEN}@${AWS_DOMAIN}-${AWS_ACCOUNT_ID}.d.codeartifact.${AWS_REGION}.amazonaws.com/pypi/${AWS_CODEARTIFACT_REPOSITORY}/simple/"

COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/*

COPY scripts/run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

CMD ["/app/run.sh"]

