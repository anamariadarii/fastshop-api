FROM python:3.12-slim AS base
WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt && pip install alembic "psycopg[binary]"

COPY ./app ./app
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

EXPOSE 8000
CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"

