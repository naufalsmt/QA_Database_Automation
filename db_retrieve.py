import psycopg

connection = psycopg.connect(
    host='localhost',
    port=5432,
    dbname='qa_automation_db',
    user='postgres',
    password='admin0210'
)

print('Database connected successfully')
cursor = connection.cursor()

query = """
        SELECT * FROM employees ORDER BY employee_id
        """

cursor.execute(query)
records = cursor.fetchall()

for record in records:
    print(record)

cursor.close()
connection.close()