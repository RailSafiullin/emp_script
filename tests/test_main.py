import sys
import pytest
import argparse
from pathlib import Path
from src.main import parse_args
from src.main import REPORTS

def test_parse_args_minimal(monkeypatch):
    file1 = "/path/to/data1.csv"
    file2 = "/path/to/data2.csv"
    monkeypatch.setattr(sys, "argv", ["prog", file1, file2, "--report", "payout"])
    
    args = parse_args()
    
    assert len(args.files) == 2
    assert all(isinstance(f, Path) for f in args.files)
    assert args.files[0] == Path(file1)
    assert args.files[1] == Path(file2)
    
    assert args.report == "payout"

def test_parse_args_single_file(monkeypatch):
    single = "/only/one.csv"
    monkeypatch.setattr(sys, "argv", ["prog", single, "--report", "payout"])
    
    args = parse_args()
    assert len(args.files) == 1
    assert args.files[0] == Path(single)
    assert args.report == "payout"

@pytest.mark.parametrize("bad_report", ["", "unknown", "123"])
def test_parse_args_invalid_report(bad_report, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "f.csv", "--report", bad_report])
    with pytest.raises(SystemExit) as excinfo:
        parse_args()
    assert excinfo.value.code == 2

def test_parse_args_missing_report(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "data.csv"])
    with pytest.raises(SystemExit) as excinfo:
        parse_args()
    assert excinfo.value.code == 2

def test_parse_args_choices_match_reports_dict(monkeypatch):
    any_report = next(iter(REPORTS.keys()))
    monkeypatch.setattr(sys, "argv", ["prog", "a.csv", "--report", any_report])
    args = parse_args()
    assert args.report == any_report
