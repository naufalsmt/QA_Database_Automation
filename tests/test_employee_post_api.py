import requests
from database import get_db_connection
from uuid import uuid4

employee_id = None
def test_create_employee_api():
    employee_name = f'Test_QA_{uuid4().hex[:8]}'
    payload = {
        'employee_name': employee_name,
        'department': 'Sales Head',
        'salary': 10000
    }

    url ='http://127.0.0.1:8000/employees'
    response = requests.post(url, json=payload)
    assert response.status_code == 201, f'expect 201, but got {response.status_code}'

    post_data = response.json()
    assert post_data['employee_name'] == employee_name
    assert post_data['department'] == payload['department']
    assert post_data['salary'] == payload['salary']

    employee_id = post_data['employee_id']
    assert employee_id is not None
    assert employee_id > 0

    print('post response:',post_data)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        select_query = """
        select employee_id, employee_name, department, salary
        from employees
        where employee_id = %s;
        """
        cursor.execute(select_query, (employee_id,))
        db_data = cursor.fetchone()
        assert db_data is not None, \
            f'employee id {employee_id} not found in database'
        print('employee data:',db_data)

        assert post_data['employee_id'] == db_data[0], (
            f'Employee ID mismatch: '
            f'API = {post_data["employee_id"]}, DB = {db_data[0]}'
        )
        assert post_data['employee_name'] == db_data[1], (
            f'Employee name mismatch: '
            f'API = {post_data["employee_name"]}, DB = {db_data[1]}'
        )
        assert post_data['department'] == db_data[2], (
            f'Employee department mismatch: '
            f'API = {post_data["department"]}, DB = {db_data[2]}'
        )
        assert post_data['salary'] == db_data[3], (
            f'Employee salary mismatch: '
            f'API = {post_data["salary"]}, DB = {db_data[3]}'
        )
    finally:
        if employee_id is not None:
            cleanup_query = """
            delete from employees
            where employee_id = %s;
            """
            cursor.execute(cleanup_query, (employee_id,))
            connection.commit()
            print(f'Test employee of ID:{employee_id} cleaned up')
        cursor.close()
        connection.close()
