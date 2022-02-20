FROM python:3

WORKDIR /opt/mux-bot

COPY app/ app/
COPY setup.cfg .
COPY pyproject.toml .

RUN apt update && apt upgrade -y && apt install -y virtualenv

RUN virtualenv venv && venv/bin/pip install .

ENTRYPOINT ["/opt/mux-bot/venv/bin/mux-bot"]