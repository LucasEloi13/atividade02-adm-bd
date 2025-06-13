import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection
import random

def setup_usr_c_privileges():
    """
    Questão 4: usr_c pode recuperar ou modificar TRABALHA_EM, mas só pode recuperar
    os atributos Pnome, Minicial, Unome e Cpf de FUNCIONARIO e 
    Projnome e Projnumero de PROJETO.
    """
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Conceder privilégios completos em TRABALHA_EM
        print("Concedendo privilégios em TRABALHA_EM...")
        db.execute_query("GRANT SELECT, INSERT, UPDATE, DELETE ON TRABALHA_EM TO usr_c;")
        time.sleep(0.5)
        
        # Criar visão limitada para FUNCIONARIO
        print("Criando visão para FUNCIONARIO...")
        db.execute_query("""
            CREATE OR REPLACE VIEW vw_funcionario_usr_c AS
            SELECT Pronome, Minicial, Unome, Cpf
            FROM FUNCIONARIO;
        """)
        time.sleep(0.5)
        
        # Criar visão limitada para PROJETO
        print("Criando visão para PROJETO...")  
        db.execute_query("""
            CREATE OR REPLACE VIEW vw_projeto_usr_c AS
            SELECT Projnome, Projnumero
            FROM PROJETO;
        """)
        time.sleep(0.5)
        
        # Conceder SELECT nas visões
        print("Concedendo privilégios de SELECT nas visões...")
        db.execute_query("GRANT SELECT ON vw_funcionario_usr_c TO usr_c;")
        db.execute_query("GRANT SELECT ON vw_projeto_usr_c TO usr_c;")
        time.sleep(0.5)
        
        print("Privilégios configurados para usr_c")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_c: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_c():
    """Testa os privilégios do usr_c"""
    print("\n=== TESTANDO PRIVILÉGIOS DO usr_c ===")
    time.sleep(1)
    
    db_usr_c = DatabaseConnection()
    db_usr_c.user = 'usr_c'
    db_usr_c.password = 'usr_c123'
    conn = db_usr_c.connect()
    
    if not conn:
        print("Falha ao conectar como usr_c")
        return
    
    try:
        # Teste 1: SELECT em TRABALHA_EM (deve funcionar)
        print("\nTeste 1: SELECT em TRABALHA_EM")
        result = db_usr_c.fetch_all("SELECT * FROM TRABALHA_EM LIMIT 3;")
        if result:
            print(f"   SUCESSO: usr_c conseguiu consultar TRABALHA_EM")
            for row in result:
                print(f"     - CPF: {row['fcpf']}, Projeto: {row['pnr']}, Horas: {row['horas']}")
        time.sleep(1)
        
        # Teste 2: Tentar acessar campos não permitidos (deve falhar)
        print("\nTeste 2: Tentar acessar campos não permitidos")
        result = db_usr_c.fetch_all("SELECT Salario FROM FUNCIONARIO LIMIT 1;")
        print("   RESULTADO ESPERADO: usr_c não deve conseguir acessar Salario")
        time.sleep(1)
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_c.disconnect()

if __name__ == "__main__":
    setup_usr_c_privileges()
    test_usr_c()
