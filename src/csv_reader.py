import logging
from pathlib import Path
from typing import List
from models.employee import Employee

logger = logging.getLogger(__name__)


class CsvParser:
    """Handles CSV file parsing and data validation."""

    @classmethod
    def read_employees(cls, file_path: Path) -> List[Employee]:
        """Reads and validates employee data from CSV file.

        Args:
            file_path: Path to CSV file

        Returns:
            List of validated Employee instances

        Raises:
            RuntimeError: For critical file format issues
        """
        try:
            with file_path.open(encoding="utf-8") as f:
                lines = iter(f)
                header_line = next(lines, None)
                if header_line is None:
                    logger.warning("Empty file: %s", file_path)
                    return []

                headers = [h.strip() for h in header_line.split(",")]
                try:
                    mapper = Employee.build_mapper(headers)
                except ValueError as e:
                    logger.critical("Invalid file format in %s: %s", file_path, e)
                    raise RuntimeError(f"Invalid CSV format: {file_path}") from e

                employees = []
                for line_num, line in enumerate(lines, start=2):
                    values = line.strip().split(",")
                    if len(values) != len(headers):
                        logger.warning(
                            "Line %d: Column count mismatch, skipping", line_num
                        )
                        continue
                    try:
                        employee = Employee.from_csv_row(values, mapper)
                        employees.append(employee)
                    except ValueError as e:
                        logger.warning("Line %d: Invalid data - %s", line_num, e)

            logger.info(
                "Processed %s: %d valid records", file_path.name, len(employees)
            )
            return employees
        except FileNotFoundError:
            logger.error("File not found: %s", file_path)
            raise
