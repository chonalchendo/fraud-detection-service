FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./ 
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

# Copy app handler code
COPY producer/ /app/src/

# RUN uv pip install --system kafka-python==2.0.2 
# RUN uv pip install --system pandas
# RUN uv pip install --system pyarrow

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]

