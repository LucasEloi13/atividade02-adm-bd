#!/bin/bash

echo "Settando ambiente..."

# Install dependencies
echo "Instalando dependências..."
pip install -r requirements.txt

# Criar tabelas no banco de dados
echo "Criando tabelas no banco de dados..."
# python src/utils/create_tables.py
python src/utils/create_tables_tarefa01.py
python src/utils/create_tables_tarefa02.py

# Popular tabelas
echo "Populando banco de dados..."
python src/utils/populate_database_tarefa01.py
python src/utils/populate_database_tarefa02.py

echo "Ambiente configurado com sucesso."
