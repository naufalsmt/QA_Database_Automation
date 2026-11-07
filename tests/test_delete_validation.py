import pytest

from db_verify import actual_record


def test_delete_validation(db_connection):
    cursor = db_connection.cursor()
    try:
        delete_query = """
        delete from employees where employee_id = %s;
        """
        cursor.execute(delete_query, (2,))
        assert cursor.rowcount == 1, f'No record found'
        print(f'Employee id deleted')

        select_query = """
        select * from employees where employee_id = %s;
        """
        cursor.execute(select_query, (2,))
        act_rec = cursor.fetchone()
        assert act_rec is None
        print('No record exists in database')
    finally:
        db_connection.rollback()
        cursor.close()


def test_delete_invalid_id(db_connection):
    cursor = db_connection.cursor()
    try:
        delete_query = """
        delete from employees where employee_id = %s;
        """
        cursor.execute(delete_query, (200,))
        assert cursor.rowcount == 0
        print('No record deleted')

        select_query = """
        select * from employees where employee_id = %s;
        """
        cursor.execute(select_query, (200,))
        act_rec = cursor.fetchone()
        assert act_rec is None
        print('No record exists in database')
    finally:
        db_connection.rollback()
        cursor.close()


@pytest.mark.parametrize(
    'emp_id',
    [1,2,3]
)
def test_delete_multiple_id_parameterize(db_connection, emp_id):
    cursor = db_connection.cursor()
    try:
        delete_query = """
        delete from employees where employee_id = %s;
        """
        cursor.execute(delete_query, (emp_id,))
        assert cursor.rowcount == 1
        print(f'Employee id {emp_id} deleted')

        select_query = """
        select * from employees where employee_id = %s;
        """
        cursor.execute(select_query, (emp_id,))
        act_rec = cursor.fetchone()
        assert act_rec is None
        print(f'No record exists for employee id {emp_id} in database')
    finally:
        db_connection.rollback()
        cursor.close()