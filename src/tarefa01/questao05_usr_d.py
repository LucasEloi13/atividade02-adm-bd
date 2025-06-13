import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def setup_usr_d_privileges():
    """
    Questão 5: usr_d pode recuperar qualquer atributo de FUNCIONARIO ou DEPENDENTE
    e pode modificar DEPENDENTE.
    """
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Conceder SELECT em FUNCIONARIO
        print("Concedendo privilégios de SELECT em FUNCIONARIO...")
        db.execute_query("GRANT SELECT ON FUNCIONARIO TO usr_d;")
        time.sleep(0.5)
        
        # Conceder SELECT, INSERT, UPDATE, DELETE em DEPENDENTE
        print("Concedendo privilégios de SELECT, INSERT, UPDATE, DELETE em DEPENDENTE...")
        db.execute_query("GRANT SELECT, INSERT, UPDATE, DELETE ON DEPENDENTE TO usr_d;")
        time.sleep(0.5)
        
        print("Privilégios configurados para usr_d")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_d: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_d():
    """Testa os privilégios do usr_d"""
    print("\n=== TESTANDO PRIVILÉGIOS DO usr_d ===")
    time.sleep(1)
    
    db_usr_d = DatabaseConnection()
    db_usr_d.user = 'usr_d'
    db_usr_d.password = 'usr_d123'
    conn = db_usr_d.connect()
    
    if not conn:
        print("Falha ao conectar como usr_d")
        return
    
    try:
        # Teste 1: SELECT em FUNCIONARIO (deve funcionar)
        print("\nTeste 1: SELECT em FUNCIONARIO")
        result = db_usr_d.fetch_all("SELECT Pronome, Unome, Salario FROM FUNCIONARIO LIMIT 3;")
        if result:
            print(f"   SUCESSO: usr_d conseguiu consultar FUNCIONARIO")
            for row in result:
                print(f"     - {row['pronome']} {row['unome']} - Salário: R$ {row['salario']}")
        time.sleep(1)
        
        # Teste 2: SELECT em DEPENDENTE (deve funcionar)
        print("\nTeste 2: SELECT em DEPENDENTE")
        result = db_usr_d.fetch_all("SELECT * FROM DEPENDENTE LIMIT 3;")
        if result:
            print(f"   SUCESSO: usr_d conseguiu consultar DEPENDENTE")
            for row in result:
                print(f"     - {row['nome_dependente']} ({row['parentesco']})")
        time.sleep(1)
        
        # Teste 3: Tentar modificar FUNCIONARIO (deve falhar)
        print("\nTeste 3: Tentar modificar FUNCIONARIO")
        db_usr_d.execute_query("UPDATE FUNCIONARIO SET Salario = 1000 WHERE Cpf = '12345678901';")
        print("   RESULTADO ESPERADO: usr_d não deve conseguir modificar FUNCIONARIO")
        time.sleep(1)
        
        # Teste 5: Tentar acessar tabela não permitida (deve falhar)
        print("\nTeste 5: Tentar acessar DEPARTAMENTO")
        result = db_usr_d.fetch_all("SELECT * FROM DEPARTAMENTO LIMIT 1;")
        print("   RESULTADO ESPERADO: usr_d não deve conseguir acessar DEPARTAMENTO")
        time.sleep(1)
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_d.disconnect()

if __name__ == "__main__":
    setup_usr_d_privileges()
    test_usr_d()
