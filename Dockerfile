FROM python:3.13-slim-bookworm AS builder

ENV PIP_NO_CACHE_DIR=1
ENV SODIUM_INSTALL=system

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        build-essential \
        libffi-dev \
        libsodium-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt


FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        libffi8 \
        libsodium23 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY app ./app
COPY services ./services
COPY main.py .

RUN useradd --create-home --uid 10001 rayquaza \
    && chown -R rayquaza:rayquaza /app

USER rayquaza

CMD ["python", "main.py"]