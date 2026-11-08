import requests


def test_post_missing_department():
    url = 'http://127.0.0.1:8000/employees/'
    payload = {
        "employee_name": "Negative test name",
        "salary": 5000
    }
    req = requests.post(url, json=payload)
    assert req.status_code == 422, f'expect 422, but got {req.status_code}'

    res = req.json()
    print('Missing department validation passed')
    print('the response is:',res)


def test_post_invalid_salary():
    url = 'http://127.0.0.1:8000/employees/'
    payload = {
        "employee_name": "Negative test name",
        "department": "Negative test department",
        "salary": "ABC"
    }
    req = requests.post(url, json=payload)

    print("Status code:", req.status_code)
    print("Response body:", req.text)
    print("Request payload:", payload)

    assert req.status_code == 422, f'expect 422, but got {req.status_code}'
    res = req.json()
    print('Invalid salary validation passed')
    print('the response is:',res)


def test_duplicate_employee():
    url = 'http://127.0.0.1:8000/employees/'
    payload = {
        "employee_name": "Naufal",
        "department": "Software QA",
        "salary": 9000
    }
    req = requests.post(url, json=payload)
    print("Status code:", req.status_code)
    print("Response body:", req.text)
    assert req.status_code == 409, f'expect 409, but got {req.status_code}'

    res = req.json()
    assert res['detail'] == "Employee already exists"
    print('duplicate employee validation passed')


def test_department_with_whitespace():
    url = 'http://127.0.0.1:8000/employees/'
    payload = {
        "employee_name": "Negative test name",
        "department": " ",
        "salary": 5000
    }
    req = requests.post(url, json=payload)
    print("Status code:", req.status_code)
    print("Response body:", req.text)
    assert req.status_code == 422, f'expect 422, but got {req.status_code}'
    res = req.json()
    # for whitespace test assertion only
    assert res["detail"][0]["type"] == "value_error"
    assert "Department cannot be empty or whitespace" in res["detail"][0]["msg"]


def test_empty_department():
    url = 'http://127.0.0.1:8000/employees/'
    payload = {
        "employee_name": "Negative test name",
        "department": "",
        "salary": 5000
    }
    req = requests.post(url, json=payload)
    print("Status code:", req.status_code)
    print("Response body:", req.text)
    assert req.status_code == 422, f'expect 422, but got {req.status_code}'
    res = req.json()
    # for empty string test assertion only
    assert res["detail"][0]["type"] == "string_too_short"
