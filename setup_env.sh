#!bin/bash

echo "Settando ambiente..."

# Install dependencies
echo "Instalando dependências..."
pip install -r requirements.txt

# Criar tabelas no banco de dados
echo "Criando tabelas no banco de dados..."
python src/utils/create_tables.py

# Popular tabelas
echo "Populando database..."
python src/utils/populate_database.py

echo "Ambiente configurado com sucesso."