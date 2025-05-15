from reports.payout import PayoutReport
from reports.base import BaseReport

REPORTS = {
    'payout': PayoutReport,
    # 'dependent': DependentReport
}

def get_report(report_name: str) -> BaseReport:
    return REPORTS.get(report_name.lower())