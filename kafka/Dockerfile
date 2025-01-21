FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy app handler code
COPY kafka/stream.py stream.py
COPY feature_store/data/driver_stats_stream.parquet .


# Install dependencies
RUN pip3 install kafka-python==2.0.2
RUN pip3 install pandas
RUN pip3 install pyarrow

RUN uv pip install --system kafka-python==2.0.2 
RUN uv pip install --system pandas
RUN uv pip install --system pyarrow

CMD [ "python", "-u", "stream.py", "--mode", "setup", "--bootstrap_servers", "broker:29092"]
