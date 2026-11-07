from fastapi import FastAPI

app = FastAPI()


@app.get("/employees")
def get_employees():
    return {
        "employee_id": 1,
        "employee_name": "Naufal",
        "department": "Software QA",
        "salary": 9000
    }