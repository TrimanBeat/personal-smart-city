import psycopg2
from psycopg2.extras import execute_values

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="smartcity",
        user="postgres",
        password="1994"
    )
