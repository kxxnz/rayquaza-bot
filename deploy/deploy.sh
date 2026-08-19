#!/bin/sh

set -eu

DIRETORIO_PROJETO="/opt/rayquaza-bot"

printf '%s\n' \
    "" \
    "====================================" \
    "Iniciando deploy do Rayquaza" \
    "===================================="

cd "$DIRETORIO_PROJETO"

if ! docker network inspect homelab-network >/dev/null 2>&1; then
    printf '%s\n' "Criando rede compartilhada do homelab..."
    docker network create homelab-network
fi

printf '%s\n' "Baixando imagens atualizadas..."
docker-compose pull

printf '%s\n' "Atualizando containers..."
docker-compose up -d --remove-orphans

printf '%s\n' "Validando containers..."
docker-compose ps

printf '%s\n' \
    "" \
    "====================================" \
    "Deploy do Rayquaza finalizado" \
    "===================================="
