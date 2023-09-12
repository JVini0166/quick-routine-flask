import psycopg2
import os

def get_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    return conn

def get_all_tables():

    connection = get_connection()

    query = """
    SELECT tablename
    FROM pg_catalog.pg_tables
    WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
    """
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchall()

    return result

if __name__ == "__main__":
    main()
