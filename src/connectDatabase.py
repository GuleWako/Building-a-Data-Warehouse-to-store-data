import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)

def connect_to_database(database_name,port_number,database_user,database_password,host_name):
    try:
        conn = psycopg2.connect(
            database= database_name,
            user = database_user,
            password = database_password,
            host = host_name,
            port = port_number
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
        return df
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return None
load_dotenv()
DB_HOST = os.getenv("DB_HOST_NAME")
DB_PORT = os.getenv("DB_PORT_NUMBER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
def fetch_data_from_database():
    conn = connect_to_database(DB_NAME,DB_PORT,DB_USER,DB_PASSWORD,DB_HOST)
    if conn is not None:
        select_query = "SELECT * FROM detected_image"
        results_data = execute_query(conn, select_query)

        if results_data is not None:
            return results_data
        
        conn.close()


def export_detection_image_to_psql(data):
    # Connect to the database
    conn = connect_to_database(DB_NAME, DB_PORT, DB_USER, DB_PASSWORD, DB_HOST)
    if conn is None:
        logging.error("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        logging.info("Creating table detected_image...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS detected_image (
            id serial PRIMARY KEY,
            image VARCHAR,
            class FLOAT,
            x_center FLOAT,
            y_center FLOAT,
            width FLOAT,
            height FLOAT,
            confidence FLOAT
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        logging.info("Table creation attempted.")

        insert_query = """
        INSERT INTO detected_image (image, class, x_center, y_center, width, height, confidence)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for index, row in data.iterrows():
            logging.info(f"Processing row {index}: {row['Image']}")
            cursor.execute(insert_query, (
                row['Image'], row['Class'], row['X_Center'], row['Y_Center'],
                row['Width'], row['Height'], row['Confidence']
            ))
            logging.info(f"Data inserted for row {index}.")

        conn.commit()

    except psycopg2.Error as e:
        logging.error(f"Error executing query: {e}")
    finally:
        if conn is not None:
            conn.close()