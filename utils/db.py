import os
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

# initialise a connection pool
db_pool = pool.SimpleConnectionPool(
    1, 10,  # Min 1 connection, max 10
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD')
)

def get_db_connection():
    return db_pool.getconn()

def close_db_connection(conn):
    db_pool.putconn(conn)
