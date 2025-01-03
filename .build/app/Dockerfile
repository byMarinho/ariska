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

WORKDIR /app

RUN apt-get update -y

# Copy application files
COPY src/app /app/src/app
COPY --from=build /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:{$PATH}"
ENV PYTHONPATH="/app/src"

EXPOSE 8501

CMD ["streamlit", "run", "/app/src/app/main.py", "--server.port", "8501", "--server.address=0.0.0.0", "--server.enableCORS", "true"]   