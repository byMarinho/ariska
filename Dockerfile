FROM python:3.10.1-slim

WORKDIR /app

RUN python3 -m pip install -U pip
RUN python3 -m pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml /app/
RUN poetry install

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/main.py"]