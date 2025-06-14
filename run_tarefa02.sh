#!/bin/bash

set -e  # Para o script se houver erro

echo "=== EXECUTANDO TAREFA 02 AUTOMATICAMENTE ==="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f ".devcontainer/docker-compose.yml" ]; then
    echo "Erro: Arquivo docker-compose.yml não encontrado!"
    echo "Execute este script a partir do diretório raiz do projeto."
    exit 1
fi

# Verificar se o container está rodando
CONTAINER_NAME=$(docker-compose -f .devcontainer/docker-compose.yml ps -q app)
if [ -z "$CONTAINER_NAME" ]; then
    echo "Erro: Container não está rodando!"
    exit 1
fi

echo "Executando main.py da tarefa02..."
clear
docker exec -i $CONTAINER_NAME bash -c "
    cd /workspaces/atividade02-adm-bd/ || exit 1
    python src/tarefa02/main.py
"

echo ""
echo "=== TAREFA 02 CONCLUÍDA ==="
