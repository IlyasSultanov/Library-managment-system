# Build stage
FROM python:latest

WORKDIR /app

ENV PYTHONPATH=/app

ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false

RUN poetry build --format wheel

RUN pip install dist/*.whl --no-cache-dir

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

