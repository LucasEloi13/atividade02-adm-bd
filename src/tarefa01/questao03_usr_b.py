import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def setup_usr_b_privileges():
    """
    Questão 3: usr_B pode recuperar todos os atributos de FUNCIONARIO e DEPARTAMENTO,
    exceto Salario, Cpf_gerente e Data_inicio_gerente.
    """
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA tarefa01 TO usr_b;")
        
        # Criar visões para usr_B com colunas limitadas
        
        # Visão para FUNCIONARIO (sem Salario)
        db.execute_query("""
            CREATE OR REPLACE VIEW vw_funcionario_usr_b AS
            SELECT Pronome, Minicial, Unome, Cpf, Datanasc, Endereco, Sexo, Cpf_superior, Dnr
            FROM tarefa01.FUNCIONARIO;
        """)
        time.sleep(0.5)
        
        # Visão para DEPARTAMENTO (sem Cpf_gerente e Data_inicio_gerente)
        db.execute_query("""
            CREATE OR REPLACE VIEW vw_departamento_usr_b AS
            SELECT Dnome, Dnumero
            FROM tarefa01.DEPARTAMENTO;
        """)
        time.sleep(0.5)
        
        # Conceder SELECT nas visões
        db.execute_query("GRANT SELECT ON vw_funcionario_usr_b TO usr_b;")
        db.execute_query("GRANT SELECT ON vw_departamento_usr_b TO usr_b;")
        
        print("Visões criadas e privilégios concedidos para usr_b")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_b: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_b():
    """Testa os privilégios do usr_B"""
    print("\n=== TESTANDO PRIVILÉGIOS DO USR_B ===")
    time.sleep(1)
    
    db_usr_b = DatabaseConnection()
    db_usr_b.user = 'usr_b'
    db_usr_b.password = 'usr_b123'
    conn = db_usr_b.connect()
    
    if not conn:
        print("Falha ao conectar como usr_b")
        return
    
    try:
        # Teste 1: SELECT na visão de FUNCIONARIO (deve funcionar)
        print("\nTeste 1: SELECT na visão de FUNCIONARIO")
        result = db_usr_b.fetch_all("SELECT Pronome, Unome FROM vw_funcionario_usr_b LIMIT 3;")
        if result:
            print(f"   SUCESSO: usr_b conseguiu consultar funcionários")
            for row in result:
                print(f"     - {row['pronome']} {row['unome']}")
        time.sleep(1)
        
        # Teste 2: SELECT na visão de DEPARTAMENTO (deve funcionar)
        print("\nTeste 2: SELECT na visão de DEPARTAMENTO")
        result = db_usr_b.fetch_all("SELECT * FROM vw_departamento_usr_b;")
        if result:
            print(f"   SUCESSO: usr_b conseguiu consultar departamentos")
            for row in result:
                print(f"     - {row['dnome']} (ID: {row['dnumero']})")
        time.sleep(1)
        
        # Teste 3: Tentar acessar tabela original FUNCIONARIO (deve falhar)
        print("\nTeste 3: Tentar acessar tabela original FUNCIONARIO")
        result = db_usr_b.fetch_all("SELECT Salario FROM tarefa01.FUNCIONARIO LIMIT 1;")
        print("   RESULTADO ESPERADO: usr_b não deve conseguir acessar Salario")
        
        # Teste 4: Tentar acessar tabela original DEPARTAMENTO (deve falhar)
        print("\nTeste 4: Tentar acessar tabela original DEPARTAMENTO")
        result = db_usr_b.fetch_all("SELECT Cpf_gerente FROM tarefa01.DEPARTAMENTO LIMIT 1;")
        print("   RESULTADO ESPERADO: usr_b não deve conseguir acessar Cpf_gerente")
        time.sleep(1)

    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_b.disconnect()

if __name__ == "__main__":
    setup_usr_b_privileges()
    test_usr_b()
