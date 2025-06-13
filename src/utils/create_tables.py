from database_connection import DatabaseConnection

def create_tables():
    """Cria todas as tabelas do esquema"""
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return
    
    # SQL para criação das tabelas
    tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS DEPARTAMENTO (
            Dnome VARCHAR(100) NOT NULL,
            Dnumero INTEGER PRIMARY KEY,
            Cpf_gerente VARCHAR(11),
            Data_inicio_gerente DATE
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS FUNCIONARIO (
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
            FOREIGN KEY (Cpf_superior) REFERENCES FUNCIONARIO(Cpf),
            FOREIGN KEY (Dnr) REFERENCES DEPARTAMENTO(Dnumero)
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS LOCALIZACAO_DEP (
            Dnumero INTEGER,
            Dlocal VARCHAR(100),
            PRIMARY KEY (Dnumero, Dlocal),
            FOREIGN KEY (Dnumero) REFERENCES DEPARTAMENTO(Dnumero)
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS PROJETO (
            Projnome VARCHAR(100) NOT NULL,
            Projnumero INTEGER PRIMARY KEY,
            Projlocal VARCHAR(100),
            Dnum INTEGER,
            FOREIGN KEY (Dnum) REFERENCES DEPARTAMENTO(Dnumero)
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS TRABALHA_EM (
            Fcpf VARCHAR(11),
            Pnr INTEGER,
            Horas DECIMAL(4,1),
            PRIMARY KEY (Fcpf, Pnr),
            FOREIGN KEY (Fcpf) REFERENCES FUNCIONARIO(Cpf),
            FOREIGN KEY (Pnr) REFERENCES PROJETO(Projnumero)
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS DEPENDENTE (
            Fcpf VARCHAR(11),
            Nome_dependente VARCHAR(100),
            Sexo CHAR(1) CHECK (Sexo IN ('M', 'F')),
            Datanasc DATE,
            Parentesco VARCHAR(50),
            PRIMARY KEY (Fcpf, Nome_dependente),
            FOREIGN KEY (Fcpf) REFERENCES FUNCIONARIO(Cpf)
        );
        """,
        
        # Adicionar FK do gerente após criar FUNCIONARIO
        """
        ALTER TABLE DEPARTAMENTO 
        DROP CONSTRAINT IF EXISTS fk_departamento_gerente;
        """,
        
        """
        ALTER TABLE DEPARTAMENTO 
        ADD CONSTRAINT fk_departamento_gerente 
        FOREIGN KEY (Cpf_gerente) REFERENCES FUNCIONARIO(Cpf);
        """
    ]
    
    try:
        for sql in tables_sql:
            db.execute_query(sql)
        print("Todas as tabelas foram criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    create_tables()
