FROM python:3.10-slim
WORKDIR /app
COPY timetable .
COPY .venv .
