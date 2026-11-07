import psycopg

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="qa_automation_db",
    user='postgres',
    password='admin0210',
)
print('Database connected successfully!')
connection.close()