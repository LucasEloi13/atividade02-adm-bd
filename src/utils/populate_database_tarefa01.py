from database_connection import DatabaseConnection
from faker import Faker
import random
from datetime import date, timedelta

def populate_database_tarefa01():
    """Popula o banco de dados da Tarefa 01 com dados fictícios"""
    fake = Faker('pt_BR')
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        print("Populando banco da Tarefa 01...")
        
        # 1. Inserir DEPARTAMENTOS
        departamentos = [
            ('Recursos Humanos', 1, None, '2020-01-15'),
            ('Tecnologia da Informação', 2, None, '2019-03-10'),
            ('Vendas', 3, None, '2021-05-20'),
            ('Financeiro', 4, None, '2018-08-05'),
            ('Marketing', 5, None, '2020-11-12')
        ]
        
        for dept in departamentos:
            db.execute_query(
                "INSERT INTO tarefa01.DEPARTAMENTO (Dnome, Dnumero, Cpf_gerente, Data_inicio_gerente) VALUES (%s, %s, %s, %s)",
                dept
            )
        
        # 2. Inserir FUNCIONÁRIOS
        funcionarios_cpfs = []
        gerentes_cpfs = []
        
        # Inserir gerentes primeiro
        for i in range(5):
            cpf = fake.cpf().replace('.', '').replace('-', '')
            funcionarios_cpfs.append(cpf)
            gerentes_cpfs.append(cpf)
            
            funcionario = (
                fake.first_name(),
                fake.random_letter().upper(),
                fake.last_name(),
                cpf,
                fake.date_of_birth(minimum_age=30, maximum_age=55),
                fake.address(),
                random.choice(['M', 'F']),
                round(random.uniform(8000, 15000), 2),
                None,  # Sem superior (são gerentes)
                i + 1  # Departamento
            )
            
            db.execute_query(
                "INSERT INTO tarefa01.FUNCIONARIO (Pronome, Minicial, Unome, Cpf, Datanasc, Endereco, Sexo, Salario, Cpf_superior, Dnr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                funcionario
            )
        
        # Atualizar gerentes nos departamentos
        for i, cpf in enumerate(gerentes_cpfs):
            db.execute_query(
                "UPDATE tarefa01.DEPARTAMENTO SET Cpf_gerente = %s WHERE Dnumero = %s",
                (cpf, i + 1)
            )
        
        # Inserir funcionários subordinados
        for i in range(15):
            cpf = fake.cpf().replace('.', '').replace('-', '')
            funcionarios_cpfs.append(cpf)
            
            # Garantir que alguns funcionários sejam do departamento 3
            if i < 3:
                dept = 3
            else:
                dept = random.randint(1, 5)
            
            funcionario = (
                fake.first_name(),
                fake.random_letter().upper(),
                fake.last_name(),
                cpf,
                fake.date_of_birth(minimum_age=22, maximum_age=45),
                fake.address(),
                random.choice(['M', 'F']),
                round(random.uniform(3000, 8000), 2),
                random.choice(gerentes_cpfs),  # Superior aleatório
                dept  # Departamento
            )
            
            db.execute_query(
                "INSERT INTO tarefa01.FUNCIONARIO (Pronome, Minicial, Unome, Cpf, Datanasc, Endereco, Sexo, Salario, Cpf_superior, Dnr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                funcionario
            )
        
        # 3. Inserir LOCALIZAÇÕES DOS DEPARTAMENTOS
        localizacoes = [
            (1, 'São Paulo - SP'),
            (1, 'Rio de Janeiro - RJ'),
            (2, 'São Paulo - SP'),
            (2, 'Belo Horizonte - MG'),
            (3, 'São Paulo - SP'),
            (3, 'Porto Alegre - RS'),
            (4, 'São Paulo - SP'),
            (5, 'Rio de Janeiro - RJ')
        ]
        
        for loc in localizacoes:
            db.execute_query(
                "INSERT INTO tarefa01.LOCALIZACAO_DEP (Dnumero, Dlocal) VALUES (%s, %s)",
                loc
            )
        
        # 4. Inserir PROJETOS
        projetos = [
            ('Sistema de RH', 1, 'São Paulo - SP', 1),
            ('Portal do Cliente', 2, 'São Paulo - SP', 2),
            ('App Mobile', 3, 'Rio de Janeiro - RJ', 2),
            ('Sistema Financeiro', 4, 'São Paulo - SP', 4),
            ('Campanha Digital', 5, 'Rio de Janeiro - RJ', 5),
            ('Modernização TI', 6, 'Belo Horizonte - MG', 2),
            ('CRM Vendas', 7, 'Porto Alegre - RS', 3)
        ]
        
        for proj in projetos:
            db.execute_query(
                "INSERT INTO tarefa01.PROJETO (Projnome, Projnumero, Projlocal, Dnum) VALUES (%s, %s, %s, %s)",
                proj
            )
        
        # 5. Inserir TRABALHA_EM
        for cpf in funcionarios_cpfs:
            # Cada funcionário trabalha em 1-3 projetos
            num_projetos = random.randint(1, 3)
            projetos_selecionados = random.sample(range(1, 8), num_projetos)
            
            for proj_num in projetos_selecionados:
                horas = round(random.uniform(10, 40), 1)
                db.execute_query(
                    "INSERT INTO tarefa01.TRABALHA_EM (Fcpf, Pnr, Horas) VALUES (%s, %s, %s)",
                    (cpf, proj_num, horas)
                )
        
        # 6. Inserir DEPENDENTES
        for cpf in random.sample(funcionarios_cpfs, 12):  # 12 funcionários com dependentes
            num_dependentes = random.randint(1, 3)
            
            for i in range(num_dependentes):
                dependente = (
                    cpf,
                    fake.first_name(),
                    random.choice(['M', 'F']),
                    fake.date_of_birth(minimum_age=0, maximum_age=18),
                    random.choice(['Filho(a)', 'Cônjuge', 'Pai/Mãe'])
                )
                
                db.execute_query(
                    "INSERT INTO tarefa01.DEPENDENTE (Fcpf, Nome_dependente, Sexo, Datanasc, Parentesco) VALUES (%s, %s, %s, %s, %s)",
                    dependente
                )
        
        print("Banco de dados da Tarefa 01 populado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao popular banco de dados: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    populate_database_tarefa01()