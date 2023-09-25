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


# CREATE Operations

def create_user(username, password, email):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO users (username, password, email)
        VALUES (%s, %s, %s) RETURNING id;
    """
    cursor.execute(query, (username, password, email))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return user_id


def create_habit(name, description, category, frequency, start_date, target_date, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO habits (name, description, category, frequency, start_date, target_date, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    cursor.execute(query, (name, description, category, frequency, start_date, target_date, user_id))
    habit_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return habit_id


def create_review_template(description, period):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO review_template (description, period)
        VALUES (%s, %s) RETURNING id;
    """
    cursor.execute(query, (description, period))
    template_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return template_id


def create_task(name, description, frequency, start_date, target_date, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO tasks (name, description, frequency, start_date, target_date, user_id)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
    """
    cursor.execute(query, (name, description, frequency, start_date, target_date, user_id))
    task_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return task_id


def create_review(review_template_id, review_date):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO reviews (review_template_id, review_date)
        VALUES (%s, %s) RETURNING id;
    """
    cursor.execute(query, (review_template_id, review_date))
    review_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return review_id


def create_pomodoro(duration, date, quantity, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO pomodoro (duration, date, quantity, user_id)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """
    cursor.execute(query, (duration, date, quantity, user_id))
    pomodoro_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return pomodoro_id



# CREATE Operations END

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
