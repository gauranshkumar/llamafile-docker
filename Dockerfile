FROM python:3.9-slim-bookworm
ARG VERSION=0.6

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Path: /app
WORKDIR /app

RUN curl -sSLo /app/llamafile https://github.com/Mozilla-Ocho/llamafile/releases/download/${VERSION}/llamafile-${VERSION} && \
    chmod +x /app/llamafile

# Path: /app/requirements.txt
COPY requirements.txt requirements.txt

# Path: /app
RUN pip install -r requirements.txt

# Path: /app
COPY scripts scripts

ENTRYPOINT [ "python", "scripts/main.py" ]


