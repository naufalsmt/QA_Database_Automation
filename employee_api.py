from fastapi import FastAPI
from database import get_db_connection


app = FastAPI()

@app.get("/employees")
def read_employees():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        get_query = """
        select employee_id, employee_name, department, salary
        from employees
        order by employee_id;
        """
        cursor.execute(get_query)
        records = cursor.fetchall()
        employees = []

        for record in records:
            employees.append({
                "employee_id": record[0],
                "employee_name": record[1],
                "department": record[2],
                "salary": float(record[3])
            })
        return employees
    finally:
        cursor.close()
        connection.close()

@app.get("/employees/departments/{department}")
def get_employees_departments(department: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        get_query = """
        select employee_id, employee_name, department, salary
        from employees
        where department = %s
        order by employee_id;
            """
        cursor.execute(get_query, (department,))
        records = cursor.fetchall()
        employees = []
        for record in records:
            employees.append({
                "employee_id": record[0],
                "employee_name": record[1],
                "department": record[2],
                "salary": float(record[3])
            })
        return employees
    finally:
        cursor.close()
        connection.close()

