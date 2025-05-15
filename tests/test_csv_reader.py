import logging
from pathlib import Path

import pytest # type: ignore
from src.csv_reader import CsvParser
from src.models.employee import Employee

@pytest.fixture(autouse=True)
def cap_log(caplog):
    caplog.set_level(logging.WARNING)
    return caplog

def write_file(tmp_path, name, lines):
    f = tmp_path / name
    f.write_text("\n".join(lines))
    return f

def test_read_employees_valid_and_skips_bad(tmp_path, cap_log):
    # Create a CSV with:
    #  - valid header
    #  - one good row
    #  - one row with wrong column count
    #  - one row with invalid number
    header = "id,email,name,department,hours_worked,hourly_rate"
    good = "1,foo@bar.com,Foo,Dev,10,5"
    mismatch = "2,bad@row,MissingCols"
    invalid = "3,baz@qux.com,Baz,HR,not_a_number,20"
    csv_file = write_file(tmp_path, "emps.csv", [header, good, mismatch, invalid])

    employees = CsvParser.read_employees(csv_file)
    # Only the good row should produce an Employee
    assert len(employees) == 1
    
    emp = employees[0]
    assert emp.__class__.__name__ == "Employee"
    assert hasattr(emp, "id") and emp.id == 1
    assert hasattr(emp, "email") and emp.email == "foo@bar.com"
    # Two warnings: one for mismatch, one for invalid data
    warnings = [r for r in cap_log.records if r.levelname == "WARNING"]
    assert any("Column count mismatch" in r.getMessage() for r in warnings)
    assert any("Invalid data" in r.getMessage() for r in warnings)

def test_read_employees_file_not_found(cap_log):
    missing = Path("does_not_exist.csv")
    with pytest.raises(FileNotFoundError):
        CsvParser.read_employees(missing)
    # Should log an ERROR
    errors = [r for r in cap_log.records if r.levelname == "ERROR"]
    assert any("File not found" in r.getMessage() for r in errors)
