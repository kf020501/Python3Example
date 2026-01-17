FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3.12 python3.12-venv python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN python3.12 -m venv /opt/.venv \
  && /opt/.venv/bin/pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN /opt/.venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

ENV VIRTUAL_ENV=/opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"

ENV HOME=/workspace
WORKDIR /workspace

CMD ["bash"]
