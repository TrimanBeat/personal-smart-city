import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        database=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASS"),
        port=os.getenv("PG_PORT")
    )
    return conn
