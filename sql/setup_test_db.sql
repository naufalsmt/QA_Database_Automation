
CREATE TABLE employees
(
    employee_id SERIAL PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10,2),

    CONSTRAINT unique_employee_name UNIQUE (employee_name),
    CONSTRAINT department_not_empty
        CHECK (TRIM(department) <> '')
);

INSERT INTO employees (employee_id, employee_name, department, salary)
VALUES
    (1, 'Naufal', 'Software QA', 9000),
    (2, 'Kunal', 'Solution Architecture', 19000),
    (3, 'Karthik', 'QA Engineer', 12000);

-- Keep the serial sequence aligned with the inserted IDs.
SELECT setval(
    pg_get_serial_sequence('employees', 'employee_id'),
    (SELECT MAX(employee_id) FROM employees)
);
