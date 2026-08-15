#!/bin/sh

set -eu

DIRETORIO_PROJETO="/opt/rayquaza-bot"

printf '%s
'     ""     "===================================="     "Iniciando deploy do Rayquaza"     "===================================="

cd "$DIRETORIO_PROJETO"

printf '%s
' "Baixando imagens atualizadas..."
docker compose pull

printf '%s
' "Atualizando containers..."
docker compose up -d --remove-orphans

printf '%s
' "Validando containers..."
docker compose ps

printf '%s
'     ""     "===================================="     "Deploy do Rayquaza finalizado"     "===================================="
