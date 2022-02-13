FROM fedora-minimal:latest

WORKDIR /opt/mux-bot

COPY app/ app/
COPY setup.cfg .
COPY pyproject.toml .

RUN microdnf -y install python3.10 && microdnf clean all

RUN python3 -m venv venv
RUN venv/bin/pip install -U pip
RUN venv/bin/pip install .

ENTRYPOINT ["/opt/mux-bot/venv/bin/main"]