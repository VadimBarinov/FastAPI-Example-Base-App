FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /api

RUN pip install --upgrade pip wheel poetry
RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock .
RUN poetry install

COPY ./app/ ./app/

CMD ["python3", "app/main.py"]