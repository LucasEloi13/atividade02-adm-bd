#!/bin/bash
# filepath: /workspaces/atividade02-adm-bd/run_tarefa01_local.sh

set -e  # Para o script se houver erro

echo "=== EXECUTANDO TAREFA 01 AUTOMATICAMENTE ==="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f ".devcontainer/docker-compose.yml" ]; then
    echo "Erro: Arquivo docker-compose.yml não encontrado!"
    echo "Execute este script a partir do diretório raiz do projeto."
    exit 1
fi

# Subir os containers
echo "1. Iniciando containers Docker..."
docker-compose -f .devcontainer/docker-compose.yml up -d

# Aguardar containers ficarem prontos
echo "2. Aguardando containers ficarem prontos..."
sleep 5

# Verificar se o container está rodando
CONTAINER_NAME=$(docker-compose -f .devcontainer/docker-compose.yml ps -q app)
if [ -z "$CONTAINER_NAME" ]; then
    echo "Erro: Container não está rodando!"
    exit 1
fi

echo "3. Executando comandos dentro do container..."

# Executar comandos dentro do container
docker exec -i $CONTAINER_NAME bash -c "
    echo 'Navegando para workspaces...'
    cd /workspaces/atividade02-adm-bd/ || exit 1
    
    echo 'Tornando setup_env.sh executável...'
    chmod +x ./setup_env.sh
    
    echo 'Executando setup do ambiente...'
    ./setup_env.sh
    
    echo 'Executando main.py da tarefa01...'
    python src/tarefa01/main.py
"

echo ""
echo "=== TAREFA 01 CONCLUÍDA ==="