import psycopg2
from psycopg2 import sql
import os


def connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )


def create_tables(conn):
    """ create tables in the PostgreSQL database according to the new structure"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS user_info (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password TEXT NOT NULL,
            name VARCHAR(100),
            surname VARCHAR(100),
            email VARCHAR(150),
            login_method VARCHAR(100),
            community JSON
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS async_storage (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            habit JSON,
            revision_template JSON,
            revision JSON,
            routine JSON,
            tasks JSON,
            last_sync TIMESTAMP WITH TIME ZONE,
            FOREIGN KEY (user_id) REFERENCES user_info (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS community (
            id SERIAL PRIMARY KEY,
            community_key VARCHAR(100) NOT NULL,
            user_id INTEGER NOT NULL,
            users JSON,
            shared_habits JSON,
            FOREIGN KEY (user_id) REFERENCES user_info (id)
        )
        """
    )
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()


def delete_all_tables():
    print("Deletando tabelas!")
    conn = connection()
    cur = conn.cursor()

    # Selecionar todas as tabelas
    cur.execute("""
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
    """)

    tables = cur.fetchall()

    # Deletar todas as tabelas
    for table in tables:
        cur.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE")

    conn.commit()

    cur.close()
    conn.close()


def execute_migrations():

    conn = connection()
    try:
        create_tables(conn)
    except Exception as e:
        print("Ocorreu um erro ao executar as migrations: " + str(e))
    conn.close()
    print("Migrations executadas com sucesso")

if __name__ == "__main__":
    main()
