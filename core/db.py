import os
from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()

connection_pool = pool.SimpleConnectionPool(
    minconn = 1,
    maxconn = 10,
    dsn=os.getenv("DATABASE_URL")
)

def get_db():
    conn=connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)