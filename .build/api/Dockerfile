ARG PYTHON_BASE=3.11-slim

# Build stage
FROM python:${PYTHON_BASE} as build

WORKDIR /app

COPY pyproject.toml pdm.lock README.md ./

# Install pdm
RUN python -m pip install --upgrade pip setuptools wheel &&\
    pip install pdm

# Install dependencies
RUN pdm install --no-lock --no-editable

# Run stage
FROM python:${PYTHON_BASE}

RUN apt update -y && apt install ffmpeg -y && apt install nodejs -y
RUN mkdir -p src/tmp && chmod 777 src/tmp

WORKDIR /app

# Copy application files
COPY src/api /app/src/api
COPY --from=build /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:{$PATH}"

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]