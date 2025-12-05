# connect.py
import psycopg2
from config import load_config

def connect_db():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            print("Connected to PostgreSQL server.")
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                print("Server version:", version)
            return True
    except Exception as e:
        print("Error:", e)
        return False

if __name__ == "__main__":
    connect_db()
