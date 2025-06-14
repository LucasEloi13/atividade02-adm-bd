import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# from cleanup import cleanup_all
from create_users import create_users
from questao02_usr_a import setup_usr_a_privileges, test_usr_a
from questao03_usr_b import setup_usr_b_privileges, test_usr_b
from questao04_usr_c import setup_usr_c_privileges, test_usr_c
from questao05_usr_d import setup_usr_d_privileges, test_usr_d
from questao06_usr_e import setup_usr_e_privileges, test_usr_e


def verify_users_created():
    """Verifica se os usuários foram criados corretamente"""
    from utils.database_connection import DatabaseConnection
    
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        # Verificar se os usuários existem (nomes em minúscula)
        result = db.fetch_all("""
            SELECT usename FROM pg_user 
            WHERE usename IN ('usr_a', 'usr_b', 'usr_c', 'usr_d', 'usr_e')
            ORDER BY usename;
        """)
        
        if result:
            print("   Usuários encontrados no sistema:")
            for row in result:
                print(f"     - {row['usename']}")
            return len(result) == 5
        else:
            print("   Nenhum usuário encontrado!")
            return False
            
    except Exception as e:
        print(f"Erro ao verificar usuários: {e}")
        return False
    finally:
        db.disconnect()

def main():
    """Executa todos os testes de controle de acesso"""
    print("=== INICIANDO CONFIGURAÇÃO DE CONTROLE DE ACESSO ===\n")
    
    # # Passo 0: Limpeza do ambiente
    # print("0. Limpando ambiente anterior...")
    # cleanup_all()
    # time.sleep(3)
    
    # print("\n" + "="*60)
    
    # Passo 1: Criar usuários
    print("1. Criando usuários...")
    if not create_users():
        print("Erro ao criar usuários. Abortando.")
        return
    
    # Verificar se os usuários foram criados
    print("\n   Verificando usuários criados...")
    if not verify_users_created():
        print("Erro: Usuários não foram criados corretamente. Abortando.")
        return
    
    time.sleep(2)
    print("\n" + "="*60)
    
    # Passo 2: Configurar e testar usr_a
    print("2. Configurando e testando usr_a...")
    time.sleep(1)
    if setup_usr_a_privileges():
        time.sleep(1)
        test_usr_a()
    
    time.sleep(3)
    print("\n" + "="*60)
    
    # Passo 3: Configurar e testar usr_b
    print("3. Configurando e testando usr_b...")
    time.sleep(1)
    if setup_usr_b_privileges():
        time.sleep(1)
        test_usr_b()
    
    time.sleep(3)
    print("\n" + "="*60)
    
    # Passo 4: Configurar e testar usr_c
    print("4. Configurando e testando usr_c...")
    time.sleep(1)
    if setup_usr_c_privileges():
        time.sleep(1)
        test_usr_c()
    
    time.sleep(3)
    print("\n" + "="*60)
    
    # Passo 5: Configurar e testar usr_d
    print("5. Configurando e testando usr_d...")
    time.sleep(1)
    if setup_usr_d_privileges():
        time.sleep(1)
        test_usr_d()
    
    time.sleep(3)
    print("\n" + "="*60)
    
    # Passo 6: Configurar e testar usr_e
    print("6. Configurando e testando usr_e...")
    time.sleep(1)
    if setup_usr_e_privileges():
        time.sleep(1)
        test_usr_e()
    
    time.sleep(2)
    print("\n" + "="*60)
    print("=== TESTES DE CONTROLE DE ACESSO CONCLUÍDOS ===")

if __name__ == "__main__":
    main()
