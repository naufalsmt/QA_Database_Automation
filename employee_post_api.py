from fastapi import FastAPI, HTTPException
from database import get_db_connection
from pydantic import BaseModel, Field, field_validator
import psycopg

app = FastAPI()

class EmployeeCreate(BaseModel):
    employee_name: str
    department: str = Field(min_length=1)
    salary: float

    @field_validator('department')
    @classmethod
    def department_validator(cls, value):
        if not value.strip():
            raise ValueError("Department cannot be empty or whitespace")
        return value


@app.post('/employees/', status_code=201)
def post_employee_create(employee: EmployeeCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        insert_query = """
        INSERT INTO employees (employee_name, department, salary)
        values (%s, %s, %s)
        returning employee_id, employee_name, department, salary;
            """
        cursor.execute(
            insert_query,
            (employee.employee_name, employee.department, employee.salary)
        )
        response = cursor.fetchone()
        connection.commit()
        return {
            'employee_id': response[0],
            'employee_name': response[1],
            'department': response[2],
            'salary': response[3]
        }

    except psycopg.errors.UniqueViolation:
        connection.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employee already exists"
        )

    except psycopg.errors.CheckViolation:
        connection.rollback()
        raise HTTPException(
            status_code=422,
            detail="Department cannot be empty"
        )

    finally:
        cursor.close()
        connection.close()