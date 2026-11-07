import pytest


def test_employee(db_connection):
    cursor = db_connection.cursor()

    query = """
            select * from employees
            order by employee_id;
                """

    cursor.execute(query)

    rows = cursor.fetchall()

    assert len(rows) >= 1
    print(rows)
    cursor.close()


def test_employee_details(db_connection):
    cursor = db_connection.cursor()

    try:
        query = """
        select employee_name, department, salary from employees
        where employee_id = %s;
        """
        cursor.execute(query, (1,))
        actual_data = cursor.fetchone()
        print(actual_data)

        assert actual_data is not None, f'employee details not exist'
        assert actual_data[0] == 'Naufal', f'employee name mismatch'
        assert actual_data[1] == 'Software QA', f'employee department mismatch'
        assert actual_data[2] == 9000, f'employee salary mismatch'
    finally:
        cursor.close()


@pytest.mark.parametrize(
    'employee_id, exp_name, exp_depart, exp_salary',
    [
        (1, 'Naufal', 'Software QA', 9000),
        (2, 'Kunal', 'Solution Architecture', 19000)
    ]
)
def test_multiple_cases(
        db_connection,
        employee_id,
        exp_name,
        exp_depart,
        exp_salary
):
    cursor = db_connection.cursor()
    try:
        query = """
        select employee_name, department, salary
        from employees
        where employee_id = %s;
            """
        cursor.execute(query, (employee_id,))
        actual_data = cursor.fetchone()
        print(actual_data)
        assert actual_data is not None, f'employee details not exist'
        assert actual_data[0] == exp_name, f'employee name mismatch'
        assert actual_data[1] == exp_depart, f'employee department mismatch'
        assert actual_data[2] == exp_salary, f'employee salary mismatch'
    finally:
        cursor.close()


def test_query_rollback(db_connection):
    cursor = db_connection.cursor()
    try:
        insert_query = """
        insert into employees
        (employee_name, department, salary)
        values (%s, %s, %s)
        returning employee_id;
        """
        employee_data = (
            "Iswarya", "Software QA", 6000
        )
        cursor.execute(insert_query, employee_data)
        employee_id = cursor.fetchone()[0]
        print("Employee id:",employee_id)
        db_connection.rollback()
        print("Insertion roll backed")

        select_query = """
        select * from employees
        where employee_id = %s;
        """
        cursor.execute(select_query, (employee_id,))
        actual_data = cursor.fetchone()
        print(actual_data)
        assert actual_data is None, f'employee details exist with id: {employee_id}'
    finally:
        cursor.close()