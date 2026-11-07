import pytest
import psycopg
from database import get_db_connection


"""
@pytest.fixture
def db_connection():
    connection = psycopg.connect(
        host='localhost',
        port=5432,
        dbname='qa_automation_db',
        user='postgres',
        password='admin0210'
    )
    yield connection

    connection.close()
    """

# already configured the connection in database.py file. so her re-use it.
@pytest.fixture
def db_connection():
    connection = get_db_connection()
    yield connection
    connection.close()