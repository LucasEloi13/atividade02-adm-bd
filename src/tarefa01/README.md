# Tarefa 01 - Controle de Acesso no PostgreSQL

Este diretório contém scripts para implementar e testar políticas de controle de acesso conforme especificado nas questões.

## Estrutura dos Arquivos

- `create_users.py` - Cria os usuários necessários (usr_A, usr_B, usr_C, usr_D, usr_E)
- `questao02_usr_a.py` - Configura privilégios para usr_A
- `questao03_usr_b.py` - Configura privilégios para usr_B
- `questao04_usr_c.py` - Configura privilégios para usr_C
- `questao05_usr_d.py` - Configura privilégios para usr_D
- `questao06_usr_e.py` - Configura privilégios para usr_E
- `main.py` - Script principal que executa todos os testes

## Como Executar

1. Certifique-se de que o banco de dados está populado:
   ```bash
   cd /workspaces/postgres
   python src/utils/create_tables.py
   python src/utils/populate_database.py
   ```

2. Execute os testes de controle de acesso:
   ```bash
   cd src/tarefa01
   python main.py
   ```

## Políticas Implementadas

### usr_A (Questão 2)
- Pode recuperar ou modificar qualquer tabela, exceto DEPENDENTE
- Pode conceder privilégios a outros usuários (WITH GRANT OPTION)

### usr_B (Questão 3)
- Pode recuperar todos os atributos de FUNCIONARIO e DEPARTAMENTO
- Exceto: Salario, Cpf_gerente, Data_inicio_gerente
- Implementado através de visões limitadas

### usr_C (Questão 4)
- Pode recuperar ou modificar TRABALHA_EM
- Pode recuperar apenas Pnome, Minicial, Unome, Cpf de FUNCIONARIO
- Pode recuperar apenas Projnome, Projnumero de PROJETO
- Implementado através de visões limitadas

### usr_D (Questão 5)
- Pode recuperar qualquer atributo de FUNCIONARIO ou DEPENDENTE
- Pode modificar DEPENDENTE

### usr_E (Questão 6)
- Pode recuperar qualquer atributo de FUNCIONARIO
- Apenas para funcionários com Dnr = 3
- Implementado através de visão com filtro

## Testes Realizados

Cada script realiza testes de:
- ✓ Casos de sucesso (operações permitidas)
- ✓ Casos de falha (operações negadas)
- ✓ Verificação de restrições específicas
