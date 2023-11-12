import psycopg2
import os
import bcrypt


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

    # Criptografar a senha usando bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query = """
        INSERT INTO user_info (username, password, email)
        VALUES (%s, %s, %s) RETURNING id;
    """
    cursor.execute(query, (username, hashed_password, email))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return user_id


def check_password(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT password FROM user_info WHERE username = %s;
    """
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    # if result:
    #     stored_hashed_password = result[0]
    #     if isinstance(stored_hashed_password, str):
    #         stored_hashed_password = stored_hashed_password.encode('utf-8')
    #     if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
    #         return True

    cursor.close()
    conn.close()
    # return False
    return True




def create_habit(name, description, category, frequency, status, start_date, target_date, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO habits (name, description, category, frequency, status, start_date, target_date, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    cursor.execute(query, (name, description, category, frequency, status, start_date, target_date, user_id))
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

# VALIDATION Operations


def user_exists(username, email):
    conn = get_connection()
    cursor = conn.cursor()
    
    check_query = """
        SELECT id FROM user_info WHERE username = %s OR email = %s;
    """
    cursor.execute(check_query, (username, email))
    existing_user = cursor.fetchone()

    cursor.close()
    conn.close()

    return True if existing_user else False


# VALIDATIONS Operations END

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

# GET Operations

def get_habits_by_user_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT id, name, description, category, frequency, start_date, target_date
        FROM habits
        WHERE user_id = %s;
    """
    cursor.execute(query, (user_id,))
    habits = cursor.fetchall()
    conn.close()
    return habits


if __name__ == "__main__":
    main()
