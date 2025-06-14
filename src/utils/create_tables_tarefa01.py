from database_connection import DatabaseConnection

def create_tables_tarefa01():
    """Cria todas as tabelas do esquema da Tarefa 01"""
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    # SQL para criação do schema e tabelas
    tables_sql = [
        """
        DROP SCHEMA IF EXISTS tarefa01 CASCADE;
        """,
        
        """
        CREATE SCHEMA tarefa01;
        """,
        
        """
        CREATE TABLE tarefa01.DEPARTAMENTO (
            Dnome VARCHAR(100) NOT NULL,
            Dnumero INTEGER PRIMARY KEY,
            Cpf_gerente VARCHAR(11),
            Data_inicio_gerente DATE
        );
        """,
        
        """
        CREATE TABLE tarefa01.FUNCIONARIO (
            Pronome VARCHAR(50) NOT NULL,
            Minicial CHAR(1),
            Unome VARCHAR(50) NOT NULL,
            Cpf VARCHAR(11) PRIMARY KEY,
            Datanasc DATE,
            Endereco VARCHAR(200),
            Sexo CHAR(1) CHECK (Sexo IN ('M', 'F')),
            Salario DECIMAL(10,2),
            Cpf_superior VARCHAR(11),
            Dnr INTEGER,
            FOREIGN KEY (Cpf_superior) REFERENCES tarefa01.FUNCIONARIO(Cpf),
            FOREIGN KEY (Dnr) REFERENCES tarefa01.DEPARTAMENTO(Dnumero)
        );
        """,
        
        """
        CREATE TABLE tarefa01.LOCALIZACAO_DEP (
            Dnumero INTEGER,
            Dlocal VARCHAR(100),
            PRIMARY KEY (Dnumero, Dlocal),
            FOREIGN KEY (Dnumero) REFERENCES tarefa01.DEPARTAMENTO(Dnumero)
        );
        """,
        
        """
        CREATE TABLE tarefa01.PROJETO (
            Projnome VARCHAR(100) NOT NULL,
            Projnumero INTEGER PRIMARY KEY,
            Projlocal VARCHAR(100),
            Dnum INTEGER,
            FOREIGN KEY (Dnum) REFERENCES tarefa01.DEPARTAMENTO(Dnumero)
        );
        """,
        
        """
        CREATE TABLE tarefa01.TRABALHA_EM (
            Fcpf VARCHAR(11),
            Pnr INTEGER,
            Horas DECIMAL(4,1),
            PRIMARY KEY (Fcpf, Pnr),
            FOREIGN KEY (Fcpf) REFERENCES tarefa01.FUNCIONARIO(Cpf),
            FOREIGN KEY (Pnr) REFERENCES tarefa01.PROJETO(Projnumero)
        );
        """,
        
        """
        CREATE TABLE tarefa01.DEPENDENTE (
            Fcpf VARCHAR(11),
            Nome_dependente VARCHAR(100),
            Sexo CHAR(1) CHECK (Sexo IN ('M', 'F')),
            Datanasc DATE,
            Parentesco VARCHAR(50),
            PRIMARY KEY (Fcpf, Nome_dependente),
            FOREIGN KEY (Fcpf) REFERENCES tarefa01.FUNCIONARIO(Cpf)
        );
        """,
        
        # Adicionar FK do gerente após criar FUNCIONARIO
        """
        ALTER TABLE tarefa01.DEPARTAMENTO 
        DROP CONSTRAINT IF EXISTS fk_departamento_gerente;
        """,
        
        """
        ALTER TABLE tarefa01.DEPARTAMENTO 
        ADD CONSTRAINT fk_departamento_gerente 
        FOREIGN KEY (Cpf_gerente) REFERENCES tarefa01.FUNCIONARIO(Cpf);
        """
    ]
    
    try:
        print("Criando schema e tabelas da Tarefa 01...")
        for sql in tables_sql:
            db.execute_query(sql)
        print("Schema TAREFA01 e tabelas criadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    create_tables_tarefa01()
