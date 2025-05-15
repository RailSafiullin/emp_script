from typing import List, Tuple
from models.employee import Employee
from reports.base import BaseReport

class PayoutReport(BaseReport):
    def __init__(self, sort_keys: List[Tuple[str, bool]] = None):
        # Default sorting: department (asc), payout (desc), name (asc)
        default_keys = [("department", False), ("payout", True), ("name", False)]
        super().__init__(sort_keys or default_keys)

    def _prepare_data(self, employees: List[Employee]) -> List[dict]:
        return [
            {
                "department": emp.department,
                "name": emp.name,
                "hours": emp.hours_worked,
                "rate": emp.hourly_rate,
                "payout": emp.hours_worked * emp.hourly_rate,
            }
            for emp in employees
        ]

    def _print(self, data: List[dict]) -> None:
        if not data:
            print("No data to report.")
            return
        
        group_by_department = ("department", False) in self.sort_keys or ("department", True) in self.sort_keys
        header = f"{'Department':<15} {'Name':<20} {'Hours':<8} {'Rate':<9} {'Payout':<5}"
        print(header)
        print("-" * len(header))

        last_dept = None
        for row in data:
            current_dept = row.get("department")
            # for custom printing by department
            if group_by_department:
                if current_dept != last_dept:
                    print(f"{current_dept}")
                    print("-" * len(header))
                    last_dept = current_dept
                dept = ""*15
            else:
                dept = current_dept
            print(
                f"{dept:<16}{row['name']:<20} {row['hours']:<8.0f} {row['rate']:<9.0f} ${row['payout']:<5.0f}"
            )

        print()