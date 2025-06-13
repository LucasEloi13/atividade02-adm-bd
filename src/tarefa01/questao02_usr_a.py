import sys
import os
import time
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def setup_usr_a_privileges():
    """
    Questão 2: usr_a pode recuperar ou modificar qualquer tabela, 
    exceto DEPENDENTE, e pode conceder privilégios a outros usuários.
    """
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Tabelas que usr_a pode acessar completamente
        tables = ['FUNCIONARIO', 'DEPARTAMENTO', 'LOCALIZACAO_DEP', 'PROJETO', 'TRABALHA_EM']
        
        for table in tables:
            # Conceder SELECT, INSERT, UPDATE, DELETE com opção de grant
            db.execute_query(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {table} TO usr_a WITH GRANT OPTION;")
            print(f"   Privilégios concedidos para usr_a na tabela {table}")
            time.sleep(0.3)
        
        # usr_a NÃO pode acessar DEPENDENTE
        print("   usr_a não tem privilégios na tabela DEPENDENTE (conforme especificado)")
        
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_a: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_a():
    """Testa os privilégios do usr_a"""
    print("\n=== TESTANDO PRIVILÉGIOS DO usr_a ===")
    time.sleep(1)
    
    # Criar conexão como usr_a
    db_usr_a = DatabaseConnection()
    # Modificar credenciais para usr_a
    db_usr_a.user = 'usr_a'
    db_usr_a.password = 'usr_a123'
    conn = db_usr_a.connect()

    random_id = random.randint(0, 9999)
    
    if not conn:
        print("Falha ao conectar como usr_a")
        return
    
    try:
        # Teste 1: SELECT em FUNCIONARIO (deve funcionar)
        print("\nTeste 1: SELECT em FUNCIONARIO")
        result = db_usr_a.fetch_all("SELECT COUNT(*) as total FROM FUNCIONARIO;")
        if result:
            print(f"   SUCESSO: usr_a conseguiu consultar FUNCIONARIO - {result[0]['total']} registros")
        time.sleep(1)
        
        # Teste 2: SELECT em DEPENDENTE (deve falhar)
        print("\nTeste 2: SELECT em DEPENDENTE")

        result = db_usr_a.fetch_all("SELECT COUNT(*) FROM DEPENDENTE;")
        print("   RESULTADO ESPERADO: usr_a não deve conseguir acessar DEPENDENTE")
        time.sleep(1)
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_a.disconnect()

if __name__ == "__main__":
    setup_usr_a_privileges()
    test_usr_a()
