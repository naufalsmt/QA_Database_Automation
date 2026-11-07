import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

# below connection function will work only in local
"""
def get_db_connection():
    connection = psycopg.connect(
        host="localhost",
        port="5432",
        dbname = 'qa_automation_db',
        user="postgres",
        password="admin0210"
    )
    return connection
"""


# below connection function will work in both local and in github (ci/cd)
# os.getenv() reads a value from the environment.
# means: use the environment variable DB_HOST; if it isn't set, use localhost.
def get_db_connection():
    connection = psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "qa_automation_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection