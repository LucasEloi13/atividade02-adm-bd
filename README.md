# Atividade 02 - Administração e Gerenciamento de Banco de Dados

Este projeto implementa e testa políticas de controle de acesso em PostgreSQL através de duas tarefas práticas distintas, demonstrando diferentes abordagens de segurança e gerenciamento de privilégios.

## 📋 Visão Geral do Projeto

O projeto está dividido em duas tarefas principais:

- **Tarefa 01**: Controle de acesso granular usando visões e privilégios específicos
- **Tarefa 02**: Sistema de vendas com controle baseado em roles

## 🐳 Configuração do Ambiente Docker

### Pré-requisitos
- Docker e Docker Compose instalados
- VS Code com extensão Dev Containers (opcional, porém mais fácil)

### Opção 1: Usando VS Code Dev Containers

1. Clone o repositório
2. Abra o projeto no VS Code
3. Quando solicitado, clique em "Reopen in Container"
4. Aguarde a construção do container

### Opção 2: Docker Compose Manual

```bash
# Clonar o repositório
git clone <seu-repositorio>
cd postgres

# Subir os containers
docker-compose -f .devcontainer/docker-compose.yml up -d

# Acessar o container
docker exec -it <container-name> bash
```

## ⚙️ Configuração Inicial

### Instalação Automática

Execute o script de configuração para preparar todo o ambiente:

```bash
# Dentro do container
./setup_env.sh
```

Este script irá:
- Instalar todas as dependências Python
- Criar schemas e tabelas para ambas as tarefas
- Popular o banco de dados com dados fictícios

### Instalação Manual

Se preferir executar passo a passo:

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar tabelas
python src/utils/create_tables_tarefa01.py
python src/utils/create_tables_tarefa02.py

# Popular banco de dados
python src/utils/populate_database_tarefa01.py
python src/utils/populate_database_tarefa02.py
```

## 🎯 Tarefa 01 - Controle de Acesso Granular

### Objetivo
Implementar políticas específicas de controle de acesso onde cada usuário tem privilégios customizados através de visões e restrições.

### Estrutura
```
src/tarefa01/
├── create_users.py         # Cria usuários base
├── cleanup.py             # Limpa ambiente
├── questao02_usr_a.py     # usr_a: Acesso total exceto DEPENDENTE
├── questao03_usr_b.py     # usr_b: Visões limitadas de FUNCIONARIO/DEPARTAMENTO
├── questao04_usr_c.py     # usr_c: Modifica TRABALHA_EM, consulta limitada
├── questao05_usr_d.py     # usr_d: Acesso total FUNCIONARIO/DEPENDENTE
├── questao06_usr_e.py     # usr_e: FUNCIONARIO apenas Dnr=3
└── main.py               # Execução completa
```

### Execução

#### Opção A: Teste Completo Automatizado
```bash
cd src/tarefa01
python main.py
```

#### Opção B: Execução Individual

1. **Criar usuários base:**
```bash
python create_users.py
```

2. **Executar questões individuais:**
```bash
python questao02_usr_a.py    # Teste usr_a
python questao03_usr_b.py    # Teste usr_b
python questao04_usr_c.py    # Teste usr_c
python questao05_usr_d.py    # Teste usr_d
python questao06_usr_e.py    # Teste usr_e
```

3. **Limpar ambiente (opcional):**
```bash
python cleanup.py
```

### Políticas Implementadas

| Usuário | Privilégios | Restrições |
|---------|-------------|------------|
| usr_a | Acesso total + GRANT OPTION | Não acessa DEPENDENTE |
| usr_b | FUNCIONARIO + DEPARTAMENTO | Sem Salario, Cpf_gerente, Data_inicio_gerente |
| usr_c | TRABALHA_EM completo | FUNCIONARIO/PROJETO apenas campos específicos |
| usr_d | FUNCIONARIO + DEPENDENTE | Só modifica DEPENDENTE |
| usr_e | FUNCIONARIO completo | Apenas funcionários com Dnr = 3 |

## 🏪 Tarefa 02 - Sistema de Vendas

### Objetivo
Implementar controle de acesso baseado em roles para um sistema de vendas com diferentes níveis hierárquicos.

### Estrutura
```
src/tarefa02/
├── create_roles.py        # Cria roles e atribui usuários
├── cleanup_vendasdb.py    # Limpa ambiente
├── test_admin.py          # Testa role_adm
├── test_gerente.py        # Testa role_gerente
├── test_atendente.py      # Testa role_atendente
└── main.py               # Execução completa
```

### Execução

#### Opção A: Teste Completo Automatizado
```bash
cd src/tarefa02
python main.py
```

#### Opção B: Execução Individual

1. **Criar roles e atribuir usuários:**
```bash
python create_roles.py
```

2. **Executar testes individuais:**
```bash
python test_admin.py       # Teste administrador
python test_gerente.py     # Teste gerente
python test_atendente.py   # Teste atendentes
```

3. **Limpar ambiente (opcional):**
```bash
python cleanup_vendasdb.py
```

### Roles Implementadas

| Role | Usuário | Privilégios | Tabelas de Acesso |
|------|---------|-------------|-------------------|
| role_adm | usr_a | Acesso total | Todas |
| role_gerente | usr_b | Leitura/Escrita | supplier, product, orders, orderitem |
| role_atendente | usr_c, usr_d, usr_e | Apenas leitura | customer, orders, orderitem |

## 🧪 Testes Implementados

### Tarefa 01
- ✅ Verificação de privilégios específicos por usuário
- ✅ Testes de bloqueio de acesso a tabelas/campos restritos
- ✅ Validação de GRANT OPTION
- ✅ Verificação de visões com filtros

### Tarefa 02
- ✅ Inserção de produtos pelo gerente
- ✅ Consulta de clientes pelo atendente
- ✅ Tentativa de exclusão por atendente (erro esperado)
- ✅ Verificação de hierarquia de roles

## 🗂️ Estrutura do Projeto

```
/workspaces/postgres/
├── .devcontainer/
│   ├── docker-compose.yml
│   └── Dockerfile
├── src/
│   ├── utils/
│   │   ├── database_connection.py
│   │   ├── create_tables_tarefa01.py
│   │   ├── create_tables_tarefa02.py
│   │   ├── populate_database_tarefa01.py
│   │   └── populate_database_tarefa02.py
│   ├── tarefa01/
│   │   └── [arquivos da tarefa 01]
│   └── tarefa02/
│       └── [arquivos da tarefa 02]
├── SQL/
│   ├── vendasbd.sql
│   └── popular_vendasbd.sql
├── .env
├── requirements.txt
├── setup_env.sh
└── README.md
```

## 🔧 Configurações do Banco

### Credenciais Padrão
```
Host: localhost
Porta: 5432
Usuário: postgres
Senha: postgres
Database: postgres
```

### Schemas Utilizados
- **tarefa01**: Esquema da empresa com funcionários, departamentos, projetos
- **vendasdb**: Sistema de vendas com clientes, produtos, fornecedores

## 📝 Variáveis de Ambiente

Configure o arquivo `.env` na raiz do projeto:

```env
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_PORT=5432
```

## 🚀 Execução Rápida

Para executar todo o projeto do zero:

```bash
# 1. Configurar ambiente
./setup_env.sh

# 2. Executar Tarefa 01
cd src/tarefa01
python main.py

# 3. Executar Tarefa 02
cd ../tarefa02
python main.py
```

## 📋 Dependências

- Python 3.8+
- PostgreSQL 13+
- psycopg2-binary
- python-dotenv
- Faker

## ⚠️ Notas Importantes

1. **Ordem de Execução**: A Tarefa 02 depende dos usuários criados na Tarefa 01
2. **Limpeza Automática**: Os scripts main.py fazem limpeza automática antes da execução
3. **Transações**: Os testes usam conexões separadas para evitar problemas de transação abortada
4. **Segurança**: Este é um ambiente de desenvolvimento local, por isso as credenciais estão públicas

## 🐛 Troubleshooting

### Erro "role does not exist"
Execute primeiro a Tarefa 01 para criar os usuários base.

### Erro "permission denied"
Este é o comportamento esperado nos testes de segurança.

### Erro "current transaction is aborted"
Os scripts foram atualizados para usar conexões separadas e evitar este problema.

### Problemas de conexão
Verifique se o PostgreSQL está rodando e as credenciais no `.env` estão corretas.
