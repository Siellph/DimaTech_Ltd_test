FROM python:3.13 as base

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==2.1.3

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev \
    && echo yes | poetry cache clear . --all

FROM base AS test

RUN poetry install --no-interaction --no-ansi --with dev

USER 1001