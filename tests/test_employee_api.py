import requests

def test_get_employees():
    url = 'http://127.0.0.1:8000/employees'
    req = requests.get(url)
    assert req.status_code == 200

    res = req.json()
    assert isinstance(res, list), f'expect List but got {type(res)}'
    print('response:', res)


def test_first_employee():
    url = 'http://127.0.0.1:8000/employees'
    req = requests.get(url)
    assert req.status_code == 200

    res = req.json()
    assert isinstance(res, list), f'expect List but got {type(res)}'
    assert len(res) >= 1, f'expect 1 item but got {len(res)}'

    fist_employee = res[0]
    assert fist_employee['employee_id'] == 1, f'different id found or no id found'
    assert fist_employee['employee_name'] == 'Naufal', f'different name found'
    assert fist_employee['department'] == 'Software QA', f'different department found'
    assert fist_employee['salary'] == 9000, f'different salary found'
    print('first employee details verified successfully and its passed')


def test_empty_array_validation():
    url = 'http://127.0.0.1:8000/employees/departments/tests'
    req = requests.get(url)
    assert req.status_code == 200

    res = req.json()
    assert isinstance(res, list), f'expect List but got {type(res)}'
    assert res == [], f'expect empty list but got {res}'
    print('Negative test case verified successfully and its passed')