import argparse
import logging
from pathlib import Path
from csv_reader import CsvParser
from reports.reports_register import get_report, REPORTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def parse_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate employee salary reports",
        epilog="Example: python main.py data1.csv data2.csv  --report payout",
    )
    parser.add_argument(
        "files", nargs="+", type=Path, help="Paths to CSV files with employee data"
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=REPORTS.keys(),
        help="Type of report to generate",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    all_employees = []

    for csv_file in args.files:
        try:
            all_employees.extend(CsvParser.read_employees(csv_file))
        except (RuntimeError, FileNotFoundError) as e:
            logging.error("Skipping %s: %s", csv_file.name, e)

    # payout_report = get_report(args.report)(sort_keys=[('department', True), ('payout', True), ('name', True)])

    payout_report = get_report(args.report)()
    payout_report.generate(all_employees)

    # print(payout_report._prepare_data(all_employees))


if __name__ == "__main__":
    main()
