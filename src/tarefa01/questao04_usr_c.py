import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def setup_usr_c_privileges():
    """
    Questão 4: usr_C pode recuperar ou modificar TRABALHA_EM, mas só pode recuperar
    os atributos Pnome, Minicial, Unome e Cpf de FUNCIONARIO e 
    Projnome e Projnumero de PROJETO.
    """
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Conceder privilégios completos em TRABALHA_EM
        db.execute_query("GRANT SELECT, INSERT, UPDATE, DELETE ON TRABALHA_EM TO usr_C;")
        time.sleep(0.5)
        
        # Criar visão limitada para FUNCIONARIO
        db.execute_query("""
            CREATE OR REPLACE VIEW vw_funcionario_usr_c AS
            SELECT Pronome, Minicial, Unome, Cpf
            FROM FUNCIONARIO;
        """)
        time.sleep(0.5)
        
        # Criar visão limitada para PROJETO
        db.execute_query("""
            CREATE OR REPLACE VIEW vw_projeto_usr_c AS
            SELECT Projnome, Projnumero
            FROM PROJETO;
        """)
        time.sleep(0.5)
        
        # Conceder SELECT nas visões
        db.execute_query("GRANT SELECT ON vw_funcionario_usr_c TO usr_C;")
        db.execute_query("GRANT SELECT ON vw_projeto_usr_c TO usr_C;")
        
        print("Privilégios configurados para usr_C")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar privilégios para usr_C: {e}")
        return False
    finally:
        db.disconnect()

def test_usr_c():
    """Testa os privilégios do usr_C"""
    print("\n=== TESTANDO PRIVILÉGIOS DO USR_C ===")
    time.sleep(1)
    
    db_usr_c = DatabaseConnection()
    db_usr_c.user = 'usr_C'
    db_usr_c.password = 'usr_C123'
    conn = db_usr_c.connect()
    
    if not conn:
        print("Falha ao conectar como usr_C")
        return
    
    try:
        # Teste 1: SELECT em TRABALHA_EM (deve funcionar)
        print("\nTeste 1: SELECT em TRABALHA_EM")
        result = db_usr_c.fetch_all("SELECT * FROM TRABALHA_EM LIMIT 3;")
        if result:
            print(f"   SUCESSO: usr_C conseguiu consultar TRABALHA_EM")
            for row in result:
                print(f"     - CPF: {row['fcpf']}, Projeto: {row['pnr']}, Horas: {row['horas']}")
        time.sleep(1)
        
        # Teste 2: INSERT em TRABALHA_EM (deve funcionar)
        print("\nTeste 2: INSERT em TRABALHA_EM")
        # Pegar um CPF e projeto existentes
        func_result = db_usr_c.fetch_all("SELECT Cpf FROM vw_funcionario_usr_c LIMIT 1;")
        proj_result = db_usr_c.fetch_all("SELECT Projnumero FROM vw_projeto_usr_c LIMIT 1;")
        
        if func_result and proj_result:
            cpf = func_result[0]['cpf']
            proj_num = proj_result[0]['projnumero']
            
            try:
                db_usr_c.execute_query(
                    "INSERT INTO TRABALHA_EM (Fcpf, Pnr, Horas) VALUES (%s, %s, %s);",
                    (cpf, proj_num, 5.0)
                )
                print("   SUCESSO: usr_C conseguiu inserir em TRABALHA_EM")
                # Limpar teste
                db_usr_c.execute_query("DELETE FROM TRABALHA_EM WHERE Fcpf = %s AND Pnr = %s AND Horas = 5.0;", (cpf, proj_num))
            except Exception as e:
                if "duplicate key" in str(e).lower():
                    print("   SUCESSO: usr_C tem privilégio de INSERT (registro já existe)")
                else:
                    print(f"   Erro no INSERT: {e}")
        time.sleep(1)
        
        # Teste 3: SELECT nas visões limitadas (deve funcionar)
        print("\nTeste 3: SELECT nas visões de FUNCIONARIO e PROJETO")
        func_result = db_usr_c.fetch_all("SELECT * FROM vw_funcionario_usr_c LIMIT 2;")
        proj_result = db_usr_c.fetch_all("SELECT * FROM vw_projeto_usr_c LIMIT 2;")
        
        if func_result:
            print("   SUCESSO: usr_C conseguiu consultar funcionários limitados")
        if proj_result:
            print("   SUCESSO: usr_C conseguiu consultar projetos limitados")
        time.sleep(1)
        
        # Teste 4: Tentar acessar campos não permitidos (deve falhar)
        print("\nTeste 4: Tentar acessar campos não permitidos")
        try:
            result = db_usr_c.fetch_all("SELECT Salario FROM FUNCIONARIO LIMIT 1;")
            print("   ERRO: usr_C não deveria conseguir acessar Salario")
        except Exception as e:
            print(f"   SUCESSO: usr_C foi impedido de acessar campos não permitidos")
        time.sleep(1)
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db_usr_c.disconnect()

if __name__ == "__main__":
    setup_usr_c_privileges()
    test_usr_c()
