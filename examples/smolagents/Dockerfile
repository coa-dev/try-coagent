FROM python:3.10

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

COPY ./requirements.txt /app/

RUN uv pip install --system -r requirements.txt

COPY ./src /app/src
COPY ./prompts.yaml /app/
COPY ./.env /app/.env

EXPOSE 7860

CMD python -u src/app.py
