import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv('POSTGRES_HOST')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.database = os.getenv('POSTGRES_DB')
        self.port = os.getenv('POSTGRES_PORT')
        self.connection = None

    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:

            actual_user = self.user
            
            self.connection = psycopg2.connect(
                host=self.host,
                user=actual_user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursor_factory=RealDictCursor
            )
            return self.connection
        except Exception as error:
            print(f"Erro ao conectar com PostgreSQL: {error}")
            return None

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            # print("Conexão com PostgreSQL fechada.")

    def execute_query(self, query, params=None):
        """Executa uma query no banco de dados"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except Exception as error:
            print(f"Erro ao executar query: {error}")
            try:
                self.connection.rollback()
            except Exception:
                pass  # Conexão pode estar fechada
            return None

    def execute_query_silent(self, query, params=None):
        """Executa uma query no banco de dados sem imprimir erros"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except Exception:
            try:
                self.connection.rollback()
            except Exception:
                pass  # Conexão pode estar fechada
            return None

    def fetch_all(self, query, params=None):
        """Executa uma query e retorna todos os resultados"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as error:
            print(f"Erro ao buscar dados: {error}")
            try:
                self.connection.rollback()
            except Exception:
                pass  # Conexão pode estar fechada
            return None
