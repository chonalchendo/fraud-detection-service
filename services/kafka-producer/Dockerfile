FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./ 
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

# Copy app handler code
COPY producer/ /app/src/

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]

