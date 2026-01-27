FROM python:3.9.13-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:0.8.0 /uv /uvx /bin/

RUN \
    apt-get update &&\
    apt-get install -y --no-install-recommends tini

WORKDIR /app
COPY uv.lock pyproject.toml ./
RUN uv sync --no-install-project

COPY . .

RUN uv sync

EXPOSE 8000 

ENTRYPOINT [ "tini", "--" ]
