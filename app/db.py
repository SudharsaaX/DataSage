import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def execute_query(query):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    except Exception as e:
        return {"error": str(e)}