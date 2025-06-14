import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def setup_usr_d_privileges():
    """
    Questão 5: usr_D pode recuperar qualquer atributo de FUNCIONARIO ou DEPENDENTE
    e pode modificar DEPENDENTE.
    """
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA tarefa01 TO usr_d;")
        
        # Conceder SELECT em FUNCIONARIO
        db.execute_query("GRANT SELECT ON tarefa01.FUNCIONARIO TO usr_d;")
        time.sleep(0.5)
        
        # Conceder SELECT, INSERT, UPDATE, DELETE em DEPENDENTE
        db.execute_query("GRANT SELECT, INSERT, UPDATE, DELETE ON tarefa01.DEPENDENTE TO usr_d;")
        time.sleep(0.5)
        
        print("Privilégios configurados para usr_d")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_d: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_d():
    """Testa os privilégios do usr_D"""
    print("\n=== TESTANDO PRIVILÉGIOS DO USR_D ===")
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
        result = db_usr_d.fetch_all("SELECT Pronome, Unome, Salario FROM tarefa01.FUNCIONARIO LIMIT 3;")
        if result:
            print(f"   SUCESSO: usr_d conseguiu consultar FUNCIONARIO")
            for row in result:
                print(f"     - {row['pronome']} {row['unome']} - Salário: R$ {row['salario']}")
        time.sleep(1)
        
        # Teste 2: SELECT em DEPENDENTE (deve funcionar)
        print("\nTeste 2: SELECT em DEPENDENTE")
        result = db_usr_d.fetch_all("SELECT * FROM tarefa01.DEPENDENTE LIMIT 3;")
        if result:
            print(f"   SUCESSO: usr_d conseguiu consultar DEPENDENTE")
            for row in result:
                print(f"     - {row['nome_dependente']} ({row['parentesco']})")
        else:
            print("   SUCESSO: usr_d pode acessar DEPENDENTE (sem registros)")
        time.sleep(1)
        
        # Teste 3: INSERT em DEPENDENTE (deve funcionar)
        print("\nTeste 3: INSERT em DEPENDENTE")
        # Pegar um CPF de funcionário para teste
        func_result = db_usr_d.fetch_all("SELECT Cpf FROM tarefa01.FUNCIONARIO LIMIT 1;")
        if func_result:
            cpf = func_result[0]['cpf']
            try:
                db_usr_d.execute_query(
                    "INSERT INTO tarefa01.DEPENDENTE (Fcpf, Nome_dependente, Sexo, Datanasc, Parentesco) VALUES (%s, %s, %s, %s, %s);",
                    (cpf, 'Teste usr_D', 'M', '2020-01-01', 'Filho(a)')
                )
                print("   SUCESSO: usr_d conseguiu inserir em DEPENDENTE")
                
                # Limpar teste
                db_usr_d.execute_query("DELETE FROM tarefa01.DEPENDENTE WHERE Nome_dependente = 'Teste usr_D';")
                
            except Exception as e:
                if "duplicate key" in str(e).lower():
                    print("   SUCESSO: usr_d tem privilégio de INSERT (registro já existe)")
                else:
                    print(f"   Erro no INSERT: {e}")
        time.sleep(1)
        
        # Teste 4: Tentar modificar FUNCIONARIO (deve falhar)
        print("\nTeste 4: Tentar modificar FUNCIONARIO")

        db_usr_d.execute_query("UPDATE tarefa01.FUNCIONARIO SET Salario = 1000 WHERE Cpf = '12345678901';")
        print("   RESULTADO ESPERADO: usr_d não deve conseguir modificar FUNCIONARIO")
        
        time.sleep(1)
        
        # Teste 5: Tentar acessar tabela não permitida (deve falhar)
        print("\nTeste 5: Tentar acessar DEPARTAMENTO")

        result = db_usr_d.fetch_all("SELECT * FROM tarefa01.DEPARTAMENTO LIMIT 1;")
        print("   RESULTADO ESPERADO: usr_d não deve conseguir acessar DEPARTAMENTO")

        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_d.disconnect()

if __name__ == "__main__":
    setup_usr_d_privileges()
    test_usr_d()
