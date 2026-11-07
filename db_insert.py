import psycopg

connection = psycopg.connect(
    host='localhost',
    port=5432,
    dbname='qa_automation_db',
    user='postgres',
    password='admin0210'
)

print('Database connected successfully!')
cursor = connection.cursor()

# SQL INSERT query
query = """
INSERT INTO employees
(employee_name, department, salary)
VALUES (%s, %s, %s)
"""

employee_data = (
    'Muneeb', 'UI/UX', 7500
)
cursor.execute(query, employee_data)
connection.commit()
print('Employee data inserted successfully!')

cursor.close()
connection.close()