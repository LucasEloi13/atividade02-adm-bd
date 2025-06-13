import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def setup_usr_e_privileges():
    """
    Questão 6: usr_e pode recuperar qualquer atributo de FUNCIONARIO,
    mas somente para tuplas de FUNCIONARIO que têm Dnr = 3.
    """
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Criar visão com RLS (Row Level Security) para usr_e
        print("Criando visão para FUNCIONARIO com RLS...")
        db.execute_query("""
            CREATE OR REPLACE VIEW vw_funcionario_usr_e AS
            SELECT *
            FROM FUNCIONARIO
            WHERE Dnr = 3;
        """)
        time.sleep(0.5)
        
        # Conceder SELECT na visão
        print("Concedendo privilégios de SELECT na visão...")
        db.execute_query("GRANT SELECT ON vw_funcionario_usr_e TO usr_e;")
        
        print("Privilégios configurados para usr_e")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_e: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_e():
    """Testa os privilégios do usr_e"""
    print("\n=== TESTANDO PRIVILÉGIOS DO usr_e ===")
    time.sleep(1)
    
    db_usr_e = DatabaseConnection()
    db_usr_e.user = 'usr_e'
    db_usr_e.password = 'usr_e123'
    conn = db_usr_e.connect()
    
    if not conn:
        print("Falha ao conectar como usr_e")
        return
    
    try:
        # Teste 1: SELECT na visão limitada (deve funcionar)
        print("\nTeste 1: SELECT em funcionários do departamento 3")
        result = db_usr_e.fetch_all("SELECT Pronome, Unome, Salario, Dnr FROM vw_funcionario_usr_e;")
        if result:
            print(f"   SUCESSO: usr_e conseguiu consultar funcionários do departamento 3")
            for row in result:
                print(f"     - {row['pronome']} {row['unome']} - Dept: {row['dnr']} - Salário: R$ {row['salario']}")
        else:
            print("   SUCESSO: usr_e pode acessar a visão (nenhum funcionário no dept 3)")
        time.sleep(1)
        
        # Teste 2: Tentar acessar tabela original FUNCIONARIO (deve falhar)
        print("\nTeste 2: Tentar acessar tabela original FUNCIONARIO")
        result = db_usr_e.fetch_all("SELECT COUNT(*) FROM FUNCIONARIO;")
        print("   RESULTADO ESPERADO: usr_e não deveria conseguir acessar tabela original")
        time.sleep(1)
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_e.disconnect()

if __name__ == "__main__":
    setup_usr_e_privileges()
    test_usr_e()
