import pytest
from src.models.employee import Employee

@pytest.fixture
def headers_variations():
    # all synonyms for hourly_rate should work
    return [
        ["id", "email", "name", "department", "hours_worked", "hourly_rate"],
        ["ID", "Email", "Name", "Department", "Hours_Worked", "Rate"],
        ["Id", "EMAIL", "Full Name", "Dept", "Worked Hours", "Salary"],
    ]

def test_build_mapper_success(headers_variations):
    for headers in headers_variations:
        headers = ["id","email","name","department","hours_worked", headers[-1]]
        mapper = Employee.build_mapper(headers)
        assert set(mapper.keys()) == {"id", "email", "name", "department", "hours_worked", "hourly_rate"}
        assert all(isinstance(i, int) for i in mapper.values())

def test_build_mapper_missing_header():
    # drop 'email' header → error
    headers = ["id", "name", "department", "hours_worked", "rate"]
    with pytest.raises(ValueError) as ei:
        Employee.build_mapper(headers)
    assert "Missing required header for field: email" in str(ei.value)

def test_from_csv_row_and_payout():
    headers = ["id","email","name","department","hours_worked","rate"]
    mapper = Employee.build_mapper(headers)
    row = ["42", "foo@bar.com", "Foo Bar", "Dev", " 123.5 ", " 10 "]
    emp = Employee.from_csv_row(row, mapper)
    assert emp.id == 42
    assert emp.email == "foo@bar.com"
    assert emp.name == "Foo Bar"
    assert emp.department == "Dev"
    assert emp.hours_worked == pytest.approx(123.5)
    assert emp.hourly_rate == pytest.approx(10.0)
    assert emp.payout == pytest.approx(1235.0)

def test_from_csv_row_invalid_value():
    headers = ["id","email","name","department","hours_worked","rate"]
    mapper = Employee.build_mapper(headers)
    # non-numeric hours_worked
    bad_row = ["1", "a@b.com", "A B", "HR", "not_a_number", "50"]
    with pytest.raises(ValueError):
        Employee.from_csv_row(bad_row, mapper)
