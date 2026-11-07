import psycopg

connection = psycopg.connect(
    host='localhost',
    port=5432,
    dbname='qa_automation_db',
    user='postgres',
    password='admin0210'
)

print('connection established')
cursor = connection.cursor()

expected_name = 'Naufal'
expected_department = 'Software QA'
expected_salary = 9000


query = """
SELECT * FROM employees WHERE employee_name=%s ORDER BY employee_id;"""

cursor.execute(query, (expected_name,))
actual_record = cursor.fetchone()
print(actual_record)

assert actual_record is not None, f'Employee record not found'
assert actual_record[1] == expected_name, f'Employee name should be {expected_name}'
assert actual_record[2] == expected_department, f'Employee department should be {expected_department}'
assert actual_record[3] == expected_salary, f'Employee salary should be {expected_salary}'

print('All Employee records validation passed')

cursor.close()
connection.close()