import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def setup_usr_a_privileges():
    """
    Questão 2: usr_A pode recuperar ou modificar qualquer tabela, 
    exceto DEPENDENTE, e pode conceder privilégios a outros usuários.
    """
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Tabelas que usr_A pode acessar completamente
        tables = ['FUNCIONARIO', 'DEPARTAMENTO', 'LOCALIZACAO_DEP', 'PROJETO', 'TRABALHA_EM']
        
        for table in tables:
            # Conceder SELECT, INSERT, UPDATE, DELETE com opção de grant
            db.execute_query(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {table} TO usr_A WITH GRANT OPTION;")
            print(f"   Privilégios concedidos para usr_A na tabela {table}")
            time.sleep(0.3)
        
        # usr_A NÃO pode acessar DEPENDENTE
        print("   usr_A não tem privilégios na tabela DEPENDENTE (conforme especificado)")
        
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_A: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_a():
    """Testa os privilégios do usr_A"""
    print("\n=== TESTANDO PRIVILÉGIOS DO USR_A ===")
    time.sleep(1)
    
    # Criar conexão como usr_A
    db_usr_a = DatabaseConnection()
    # Modificar credenciais para usr_A
    db_usr_a.user = 'usr_A'
    db_usr_a.password = 'usr_A123'
    conn = db_usr_a.connect()
    
    if not conn:
        print("Falha ao conectar como usr_A")
        return
    
    try:
        # Teste 1: SELECT em FUNCIONARIO (deve funcionar)
        print("\nTeste 1: SELECT em FUNCIONARIO")
        result = db_usr_a.fetch_all("SELECT COUNT(*) as total FROM FUNCIONARIO;")
        if result:
            print(f"   SUCESSO: usr_A conseguiu consultar FUNCIONARIO - {result[0]['total']} registros")
        time.sleep(1)
        
        # Teste 2: INSERT em DEPARTAMENTO (deve funcionar)
        print("\nTeste 2: INSERT em DEPARTAMENTO")
        db_usr_a.execute_query(
            "INSERT INTO DEPARTAMENTO (Dnome, Dnumero, Cpf_gerente, Data_inicio_gerente) VALUES (%s, %s, %s, %s);",
            ('Teste usr_A', 999, None, '2024-01-01')
        )
        print("   SUCESSO: usr_A conseguiu inserir em DEPARTAMENTO")
        time.sleep(1)
        
        # Teste 3: SELECT em DEPENDENTE (deve falhar)
        print("\nTeste 3: SELECT em DEPENDENTE")
        try:
            result = db_usr_a.fetch_all("SELECT COUNT(*) FROM DEPENDENTE;")
            print("   ERRO: usr_A não deveria conseguir acessar DEPENDENTE")
        except Exception as e:
            print(f"   SUCESSO: usr_A foi impedido de acessar DEPENDENTE")
        time.sleep(1)
        
        # Teste 4: Conceder privilégio a outro usuário (deve funcionar)
        print("\nTeste 4: Conceder privilégio a usr_B")
        db_usr_a.execute_query("GRANT SELECT ON FUNCIONARIO TO usr_B;")
        print("   SUCESSO: usr_A conseguiu conceder privilégio a usr_B")
        time.sleep(1)
        
        # Limpar teste
        db_usr_a.execute_query("DELETE FROM DEPARTAMENTO WHERE Dnumero = 999;")
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_a.disconnect()

if __name__ == "__main__":
    setup_usr_a_privileges()
    test_usr_a()
