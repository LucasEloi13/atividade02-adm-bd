import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cleanup_vendasdb import cleanup_vendasdb
from create_roles import create_roles, create_users
from test_admin import test_admin_permissions
from test_gerente import test_gerente_permissions
from test_atendente import test_atendente_permissions


def main():
    """Executa a configuração completa do VENDASDB"""
    print("=== INICIANDO CONFIGURAÇÃO DO VENDASDB ===\n")
    
    # Passo 1: Limpeza
    print("1. Limpando ambiente anterior...")
    cleanup_vendasdb()
    time.sleep(3)
    
    print("\n" + "="*60)

    # Passo 2: Criar roles
    print("2. Criando roles...")
    create_roles()
    create_users()
    time.sleep(1)

    print("\n" + "="*60)

    # Passo 4: Testar permissões
    print("4. Testando permissões...")
    time.sleep(1)
    
    test_admin_permissions()
    time.sleep(2)
    
    test_gerente_permissions()
    time.sleep(2)
    
    test_atendente_permissions()
    
    print("\n" + "="*60)
    print("=== CONFIGURAÇÃO DO VENDASDB CONCLUÍDA ===")

if __name__ == "__main__":
    main()
