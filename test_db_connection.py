from database import get_db_connection

connection = get_db_connection()
print('FastAPI database connection successful')
connection.close()
