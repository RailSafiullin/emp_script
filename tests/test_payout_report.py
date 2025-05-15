import pytest
from src.models.employee import Employee
from src.reports.payout import PayoutReport

@pytest.fixture
def sample_employees():
    # id, email, name, dept, hours, rate
    return [
        Employee(1, "a@mail.com", "Alice",   "Design", 100, 5),
        Employee(2, "b@mail.com", "Bob",     "Design", 200, 4),
        Employee(3, "c@mail.com", "Charlie", "Dev", 150, 6),
    ]

def test_prepare_data_fields(sample_employees):
    rpt = PayoutReport(sort_keys=[])
    data = rpt._prepare_data(sample_employees)
    
    assert len(data) == 3
    for d, emp in zip(data, sample_employees):
        assert set(d.keys()) == {"department", "name", "hours", "rate", "payout"}
        assert d["department"] == emp.department
        assert d["name"] == emp.name
        assert d["hours"] == emp.hours_worked
        assert d["rate"] == emp.hourly_rate
        assert d["payout"] == emp.payout

def test_sorting_and_print(capsys, sample_employees):

    rpt = PayoutReport(sort_keys=[("payout", True)])
    rpt.generate(sample_employees)

    out, _ = capsys.readouterr()
    raw_lines = [l for l in out.splitlines() if l.strip()]
    data_lines = raw_lines[2:]

    assert "Charlie" in data_lines[0]
    assert "Bob" in data_lines[1]
    assert "Alice" in data_lines[2]


def test_generate_default_sort_order(capsys, sample_employees):
    # default sort: department asc, payout desc, name asc
    rpt = PayoutReport()
    rpt.generate(sample_employees)
    
    out, _ = capsys.readouterr()
    lines = [l for l in out.splitlines() if l.strip()]

    assert "Design" in lines[2] and "Bob" in lines[4]
    assert "Alice" in lines[5]
    assert "Dev" in lines[6] and "Charlie" in lines[8]
