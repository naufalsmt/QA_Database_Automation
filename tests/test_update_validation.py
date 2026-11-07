import pytest


def test_update_validation(db_connection):
    cursor = db_connection.cursor()
    try:
        update_query = """
        update employees set salary = %s where employee_id = %s;
        """
        updated_salary = 9550
        cursor.execute(update_query, (updated_salary, 1,))
        print('salary updated successfully')
        assert cursor.rowcount == 1

        select_query = """
        select salary from employees where employee_id = %s;
        """
        cursor.execute(select_query, (1,))
        updated_data = cursor.fetchone()
        assert updated_data is not None
        assert updated_data[0] == updated_salary, f'different salary found'
    finally:
        db_connection.rollback()
        cursor.close()


def test_update_invalid_data(db_connection):
    cursor = db_connection.cursor()
    try:
        update_query = """
        update employees set salary = %s where employee_id = %s;
        """
        updated_salary = 12000
        cursor.execute(update_query, (updated_salary, 100,))
        assert cursor.rowcount == 0
        print('No record where updated')
    finally:
        db_connection.rollback()
        cursor.close()


@pytest.mark.parametrize(
    'salary, emp_id',
    [
        (10000, 1),
        (20000, 2),
        (30000, 3),
    ]
)
def test_update_multiple_data_parametrize(db_connection, salary, emp_id):
    cursor = db_connection.cursor()
    try:
        update_query = """
        update employees set salary = %s where employee_id = %s;
        """
        cursor.execute(update_query, (salary, emp_id,))
        assert cursor.rowcount == 1
        print(f'The employee id {emp_id} salary were updated')

        select_query = """
        select salary from employees where employee_id = %s;
        """
        cursor.execute(select_query, (emp_id,))
        updated_salary = cursor.fetchone()[0]
        print(f'Employee id {emp_id} updated salary: {updated_salary}')
        assert updated_salary == salary, f'different salary found'
    finally:
        db_connection.rollback()
        cursor.close()
