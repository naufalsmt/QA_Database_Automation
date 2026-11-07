import pytest
import psycopg


def test_duplicate_id(db_connection):
    cursor = db_connection.cursor()
    try:
        insert_query = """
        insert into employees
        (employee_id, employee_name, department, salary)
        values (%s, %s, %s, %s);
        """
        values = (1, 'Danish', 'Developer', 11500)
        with pytest.raises(psycopg.errors.UniqueViolation):
            cursor.execute(insert_query, values)
        print('duplication validated')
        db_connection.rollback()

        select_query = """
        select employee_name from employees where employee_id = %s;
        """
        cursor.execute(select_query, (1,))
        actual_data = cursor.fetchone()
        print(actual_data)
        assert actual_data is not None
        assert actual_data[0] == "Naufal"

    finally:
        cursor.close()


def test_duplicate_department(db_connection):
    cursor = db_connection.cursor()
    employee_id = None
    try:
        insert_query = """
        insert into employees
            (employee_name, department, salary)
            values (%s, %s, %s)
            returning employee_id;
        """
        values = ('Sharat', 'Software QA', 4500)
        cursor.execute(insert_query, values)
        employee_id = cursor.fetchone()[0]
        db_connection.commit()
        print('Record inserted successfully')

        select_query = """
        select count(*) from employees where department = %s;
            """
        cursor.execute(select_query, ('Software QA',))
        duplicate_count = cursor.fetchone()[0]
        print('duplicate count:', duplicate_count)
        assert duplicate_count >= 2

    finally:
        if employee_id is not None:
            delete_query = """
            delete from employees where employee_id = %s;
            """
            cursor.execute(delete_query, (employee_id,))
            print('Record deleted successfully')
            db_connection.commit()
        cursor.close()


def test_unique_employee_name(db_connection):
    cursor = db_connection.cursor()
    try:
        insert_query = """
        insert into employees
        (employee_name, department, salary)
        values (%s, %s, %s);
        """
        values = ('Kunal', 'Developer', 20500)
        with pytest.raises(psycopg.errors.UniqueViolation):
            cursor.execute(insert_query, values)
        print('Validate the employee name unique value')
        db_connection.rollback()

        select_query = """
        select employee_name from employees where employee_id = %s;
        """
        cursor.execute(select_query, (2,))
        actual_data = cursor.fetchone()
        print('Actual data is:',actual_data)
        assert actual_data is not None
        assert actual_data[0] == "Kunal"
    finally:
        cursor.close()
