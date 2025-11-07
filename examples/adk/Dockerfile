FROM python:3.13

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

COPY ./requirements.txt /app/

RUN uv pip install --system -r requirements.txt

COPY ./agent /app/agent
COPY ./.env /app/.env

EXPOSE 8000

WORKDIR /app

CMD uv run python3 -m agent
