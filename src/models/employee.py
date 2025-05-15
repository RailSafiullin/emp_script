import logging
from dataclasses import dataclass, fields
from typing import ClassVar, Dict, List, Type, TypeVar

logger = logging.getLogger(__name__)
EmployeeT = TypeVar('EmployeeT', bound='Employee')

@dataclass(slots=True)
class Employee:
    """Represents employee data with CSV parsing capabilities."""
    id: int
    email: str
    name: str
    department: str
    hours_worked: float
    hourly_rate: float

    # CSV header aliases configuration
    _CSV_ALIASES: ClassVar[Dict[str, set]] = {
        'hourly_rate': {'hourly_rate', 'rate', 'salary'}
    }
    @property
    def payout(self) -> float:
        return self.hours_worked * self.hourly_rate

    @classmethod
    def build_mapper(cls, headers: List[str]) -> Dict[str, int]:
        """Creates mapping between class fields and CSV column indices.

        Args: 
            headers: List of CSV header strings

        Returns:
            Dictionary mapping field names to column indices
            
        Raises:
            ValueError: If required headers are missing
        """
        # Convert all headings to lowercase and preserve their positions
        header_index_map = {name.strip().lower(): idx for idx, name in enumerate(headers)}
        field_to_column_map = {}

        for field in fields(cls):
            # We get possible column names for a given field
            possible_names = cls._CSV_ALIASES.get(field.name, {field.name})
            # Find first matched name
            for name in possible_names:
                if name.lower() in header_index_map:
                    field_to_column_map[field.name] = header_index_map[name.lower()]
                    break
            else:
                # No match
                logger.error(
                    "Missing required header for field '%s'. Expected one of: %s",
                    field.name,
                    ', '.join(possible_names)
                )
                raise ValueError(f"Missing required header for field: {field.name}")

        return field_to_column_map

    @classmethod
    def from_csv_row(cls: Type[EmployeeT], row: List[str], mapper: Dict[str, int]) -> EmployeeT:
        """Creates Employee instance from CSV row data.
        
        Args:
            row: List of string values from CSV row
            mapper: Field to column index mapping
            
        Returns:
            Employee instance with parsed values
            
        Raises:
            ValueError: If data conversion fails
        """
        kwargs = {}
        for field, index in mapper.items():
            try:
                raw_value = row[index].strip()
                field_type = cls.__annotations__[field]
                kwargs[field] = field_type(raw_value)
            except (IndexError, ValueError, TypeError) as e:
                logger.error("Conversion error for field %s: %s → %s", 
                            field, raw_value, field_type.__name__)
                raise ValueError(f"Invalid value for {field}: {raw_value}") from e
        return cls(**kwargs)