import requests
from database import get_db_connection

def test_api_db_validation():
    url = 'http://127.0.0.1:8000/employees/'
    req = requests.get(url)
    assert req.status_code == 200

    api_employees = req.json()
    assert len(api_employees) > 0
    print(api_employees)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        select employee_id, employee_name, department, salary
        from employees
        order by employee_id;
        """
        cursor.execute(query)
        db_records = cursor.fetchall()
        print(db_records)

        assert len(api_employees) == len(db_records), f'api records count not match with db records count'

        for api_employee, db_record in zip(api_employees, db_records):
            assert api_employee['employee_id'] == db_record[0], (
                f'Employee ID mismatch:'
                f'API={api_employee["employee_id"]}, DB={db_record[0]}'
            )
            assert api_employee['employee_name'] == db_record[1], (
                f'Employee name mismatch:'
                f'API={api_employee["employee_name"]}, DB={db_record[1]}'
            )
            assert api_employee['department'] == db_record[2], (
                f'Employee department mismatch:'
                f'API={api_employee["department"]}, DB={db_record[2]}'
            )
            assert api_employee['salary'] == db_record[3], (
                f'Employee salary mismatch:'
                f'API={api_employee["salary"]}, DB={db_record[3]}'
            )

    finally:
        connection.rollback()
        cursor.close()
        connection.close()
