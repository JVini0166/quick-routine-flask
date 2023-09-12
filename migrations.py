import psycopg2
from psycopg2 import sql
import os

def create_tables(conn):
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS habits (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            frequency VARCHAR(100),
            start_date DATE,
            target_date DATE,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS review_template (
            id SERIAL PRIMARY KEY,
            description VARCHAR(255),
            period JSONB
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            frequency VARCHAR(100),
            start_date DATE,
            target_date DATE,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            review_template_id INTEGER,
            review_date DATE,
            FOREIGN KEY (review_template_id) REFERENCES review_template (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS pomodoro (
            id SERIAL PRIMARY KEY,
            duration INTEGER,
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

def execute_migrations():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    create_tables(conn)
    conn.close()

if __name__ == "__main__":
    main()
