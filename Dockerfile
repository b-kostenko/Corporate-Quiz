FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . /app

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
