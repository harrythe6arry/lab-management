import psycopg2
from utils import auth, db

def insert_user(username, password, role):
    hashed_pw = auth.hash_password(password)  # Use hashed_password to generate the hash
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (name, password, role)
                    VALUES (%s, %s, %s)
                """, (username, hashed_pw, role))
                conn.commit()
                print("User inserted successfully")
                return True
    except psycopg2.IntegrityError as e:
        print(f"[ERROR] Integrity error: {e}")
        return False
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to insert user: {e}")
        return False

def delete(username):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE name = %s", (username,))
                conn.commit()
                return True
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to delete user: {e}")
        return False

def get_password_by_username(username):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT password FROM users WHERE name = %s
                """, (username,))
                result = cur.fetchone()
                return result[0] if result else None
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to fetch password: {e}")
        return None

def get_role_by_username(username):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT role FROM users WHERE name = %s
                """, (username,))
                result = cur.fetchone()
                return result[0] if result else None
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to fetch role: {e}")
        return None

def get_all_users():
    users = []
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, role FROM users")
                rows = cur.fetchall()
                for row in rows:
                    users.append((row[0], row[1], row[2]))
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to fetch users: {e}")
    return users