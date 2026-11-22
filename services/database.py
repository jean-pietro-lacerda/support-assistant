import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

# Conexãos simples com o banco de dados
def conectar():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )