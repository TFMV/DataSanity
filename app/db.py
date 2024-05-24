import psycopg2
from app.config import get_db_config

db_config, tables = get_db_config()

def get_connection():
    conn = psycopg2.connect(
        dbname=db_config['database'],
        user=db_config['username'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port']
    )
    return conn

def fetch_data(table_name, query):
    conn = get_connection()
    try:
        schema = db_config['schema']
        full_query = f'SET search_path TO {schema}; {query}'
        with conn.cursor() as cursor:
            cursor.execute(full_query)
            result = cursor.fetchall()
        return result
    finally:
        conn.close()
