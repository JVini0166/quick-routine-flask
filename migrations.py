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
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(500) NOT NULL,
            name VARCHAR(100),
            surname VARCHAR(100),
            email VARCHAR(100) NOT NULL
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS habits (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            frequency JSON,
            start_date DATE,
            target_date DATE,
            icon INTEGER,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS review_template (
            id SERIAL PRIMARY KEY,
            description VARCHAR(255),
            period JSON,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            recurrent BOOLEAN,
            frequency JSON,
            start_date DATE,
            target_date DATE,
            icon INTEGER,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            review_template_id INTEGER,
            review_date DATE,
            user_id INTEGER,
            FOREIGN KEY (review_template_id) REFERENCES review_template (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS pomodoro (
            id SERIAL PRIMARY KEY,
            start_time TIME,
            end_time TIME,
            date DATE,
            quantity INTEGER,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
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
