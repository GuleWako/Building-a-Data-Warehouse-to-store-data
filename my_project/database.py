import psycopg2
import os

# Load environment variables or set up DB credentials directly
DB_HOST = os.getenv("DB_HOST_NAME")
DB_PORT = os.getenv("DB_PORT_NUMBER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def connect_to_database():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn
