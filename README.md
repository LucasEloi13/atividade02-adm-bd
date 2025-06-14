# Atividade 02 - Administração e Gerenciamento de Banco de Dados

Este projeto implementa e testa políticas de controle de acesso em PostgreSQL através de duas tarefas práticas distintas, demonstrando diferentes abordagens de segurança e gerenciamento de privilégios.

## 📋 Visão Geral do Projeto

O projeto está dividido em duas tarefas principais:

- **Tarefa 01**: Controle de acesso granular usando visões e privilégios específicos
- **Tarefa 02**: Sistema de vendas com controle baseado em roles

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados
- Git

### Opção 1: Execução Rápida (Recomendada)

```bash
git clone https://github.com/LucasEloi13/atividade02-adm-bd.git
cd atividade02-adm-bd
chmod +x run_tarefa01.sh run_tarefa02.sh
```
#### Execução Tarefa01
```bash
./run_tarefa01.sh
```
#### Execução Tarefa02
```bash
./run_tarefa02.sh
```

### Opção 2: Usando VS Code Dev Container

**Pré-requisito adicional**: VS Code com extensão Dev Containers

1. Abra o projeto no VS Code
2. Quando solicitado, clique em "Reopen in Container"
3. Aguarde a construção do ambiente
4. No terminal do VS code conectado ao container, execute:

```bash
./setup_env.sh
```
5. Rode os scripts normalmente no VSCode



## 🎯 Tarefa 01 - Controle de Acesso Granular

### Objetivo
Implementar políticas específicas de controle de acesso onde cada usuário tem privilégios customizados através de visões e restrições.

### Políticas Implementadas

| Usuário | Privilégios | Restrições |
|---------|-------------|------------|
| usr_a | Acesso total + GRANT OPTION | Não acessa DEPENDENTE |
| usr_b | FUNCIONARIO + DEPARTAMENTO | Sem Salario, Cpf_gerente, Data_inicio_gerente |
| usr_c | TRABALHA_EM completo | FUNCIONARIO/PROJETO apenas campos específicos |
| usr_d | FUNCIONARIO + DEPENDENTE | Só modifica DEPENDENTE |
| usr_e | FUNCIONARIO completo | Apenas funcionários com Dnr = 3 |

## 🎯 Tarefa 02 - Sistema de Vendas

### Objetivo
Implementar controle de acesso baseado em roles para um sistema de vendas com diferentes níveis hierárquicos.

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
atividade02-adm-bd/
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
├── run_tarefa01.sh
├── run_tarefa02.sh
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
