def test_employee_validation(db_connection):
    cursor = db_connection.cursor()
    employee_id = None
    try:
        insert_query = """
                        INSERT INTO employees
                       (employee_name, department, salary)
                       values (%s, %s, %s)
                       returning employee_id;
                       """
        employee_data = (
            'Sankha', 'Web Developer', 14000
        )
        cursor.execute(insert_query, employee_data)
        employee_id = cursor.fetchone()[0]
        db_connection.commit()
        print("employee id is ", employee_id)

        select_query = """
        select employee_name, department, salary
        from employees where employee_id = %s;
            """
        cursor.execute(select_query, (employee_id,))
        actual_data = cursor.fetchone()
        assert actual_data is not None
        assert actual_data[0] == 'Sankha'
        assert actual_data[1] == 'Web Developer'
        assert actual_data[2] == 14000

    finally:
        if employee_id is not None:
            delete_query = """
            DELETE FROM employees where employee_id = %s;
                """
            cursor.execute(delete_query, (employee_id,))
            db_connection.commit()
            print("Deleted employee id with id: ", employee_id)
            cursor.close()
