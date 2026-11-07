import pytest
import psycopg


def test_department_not_null(db_connection):
    cursor = db_connection.cursor()
    try:
        insert_query = """
        insert into employees
        (employee_name, department, salary)
        values (%s, %s, %s);
            """
        walues = (
            'Haresh', None, 13200
        )
        with pytest.raises(psycopg.errors.NotNullViolation):
            cursor.execute(insert_query, walues)
        print('Null department insertion validation passed')
        db_connection.rollback()
    finally:
        cursor.close()


def test_check_empty_string(db_connection):
    cursor = db_connection.cursor()
    try:
        insert_query = """
        insert into employees
            (employee_name, department, salary)
            values (%s, %s, %s);
        """
        walues = (
            'Haresh', '   ', 13200
        )
        with pytest.raises(psycopg.errors.CheckViolation):
            cursor.execute(insert_query, walues)
        print('Empty department insertion validation passed')
        db_connection.rollback()
    finally:
        cursor.close()

