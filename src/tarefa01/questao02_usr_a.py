import sys
import os
import time
import random
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
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA tarefa01 TO usr_a;")
        
        # Tabelas que usr_A pode acessar completamente
        tables = ['FUNCIONARIO', 'DEPARTAMENTO', 'LOCALIZACAO_DEP', 'PROJETO', 'TRABALHA_EM']
        
        for table in tables:
            # Conceder SELECT, INSERT, UPDATE, DELETE com opção de grant
            db.execute_query(f"GRANT SELECT, INSERT, UPDATE, DELETE ON tarefa01.{table} TO usr_a WITH GRANT OPTION;")
            print(f"   Privilégios concedidos para usr_a na tabela {table}")
            time.sleep(0.3)
        
        # usr_A NÃO pode acessar DEPENDENTE
        print("   usr_a não tem privilégios na tabela DEPENDENTE (conforme especificado)")
        
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_a: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_a():
    """Testa os privilégios do usr_A"""
    print("\n=== TESTANDO PRIVILÉGIOS DO USR_A ===")
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
        result = db_usr_a.fetch_all("SELECT COUNT(*) as total FROM tarefa01.FUNCIONARIO;")
        if result:
            print(f"   SUCESSO: usr_a conseguiu consultar FUNCIONARIO - {result[0]['total']} registros")
        time.sleep(1)
        
        # Teste 2: INSERT em DEPARTAMENTO (deve funcionar)
        print("\nTeste 2: INSERT em DEPARTAMENTO")
        db_usr_a.execute_query(
            "INSERT INTO tarefa01.DEPARTAMENTO (Dnome, Dnumero, Cpf_gerente, Data_inicio_gerente) VALUES (%s, %s, %s, %s);",
            ('Teste usr_A', random_id, None, '2024-01-01')
        )
        print("   SUCESSO: usr_a conseguiu inserir em DEPARTAMENTO")
        time.sleep(1)
        
        # Teste 3: SELECT em DEPENDENTE (deve falhar)
        print("\nTeste 3: SELECT em DEPENDENTE")
        
        result = db_usr_a.fetch_all("SELECT COUNT(*) FROM tarefa01.DEPENDENTE;")
        print("   RESULTADO ESPERADO: usr_a não deve conseguir acessar DEPENDENTE")
        time.sleep(1)
        
        # Teste 4: Conceder privilégio a outro usuário (deve funcionar)
        print("\nTeste 4: Conceder privilégio a usr_b")
        db_usr_a.execute_query("GRANT SELECT ON tarefa01.FUNCIONARIO TO usr_b;")
        print("   SUCESSO: usr_a conseguiu conceder privilégio a usr_b")
        time.sleep(1)
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_a.disconnect()

if __name__ == "__main__":
    setup_usr_a_privileges()
    test_usr_a()
