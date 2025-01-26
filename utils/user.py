import psycopg2
from Utils import auth, db

def insert_user(username, password, role):
    hashed_password = auth.hash_password(password)  # Use a clearer function name
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (name, password, role)
                    VALUES (%s, %s, %s)
                """, (username, hashed_password, role))
                conn.commit()
                print("User inserted successfully")
                return True
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to insert user: {e}")
        return False
    finally:
        if conn:
            db.close_db_connection(conn)

def delete(username):
    conn = None
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE name = %s", (username,))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            db.close_db_connection(conn)

def get_password_by_username(username):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT password FROM users WHERE name = %s
                """, (username,))
                result = cur.fetchone()
                return result[0] if result else None  # Return password or None
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
                return result[0] if result else None  # Return role or None
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to fetch role: {e}")
        return None

def get_all_users():
    conn = None
    users = []
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, role FROM users")
        rows = cur.fetchall()
        for row in rows:
            users.append((row[0], row[1], row[2]))
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            db.close_db_connection(conn)
    return users