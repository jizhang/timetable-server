ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim

ARG POETRY_VERSION
ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install poetry==${POETRY_VERSION} && \
    $POETRY_HOME/bin/poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN $POETRY_HOME/bin/poetry install --extras gunicorn --without dev

COPY timetable/ ./timetable/
