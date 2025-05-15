import pytest
from src.reports.reports_register import get_report
from src.reports.payout import PayoutReport

def test_get_report_known():
    cls = get_report("payout")
    assert cls.__class__ == PayoutReport.__class__

def test_get_report_case_insensitive():
    cls = get_report("PAYOUT")
    assert  cls.__class__ == PayoutReport.__class__

def test_get_report_unknown():
    assert get_report("foobar") is None
