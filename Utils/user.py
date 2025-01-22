import psycopg2
from psycopg2 import sql
from . import auth
import init_db as db

def insert_user(username, password, role):
    hashed_password = auth.hashed(password)  # Clearer function name
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                insert_query = sql.SQL("""
                    INSERT INTO users (name, password, role)
                    VALUES (%s, %s, %s)
                """)
                cur.execute(insert_query, (username, hashed_password, role))
                conn.commit()
                print("User inserted successfully")
    except psycopg2.Error as e:
        print(f"Database error: {e}")

def get_password_by_username(username):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                select_query = sql.SQL("""
                    SELECT password FROM users
                    WHERE name = %s
                """)
                cur.execute(select_query, (username,))
                result = cur.fetchone()
                if result:
                    return result[0]
                else:
                    return None
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None