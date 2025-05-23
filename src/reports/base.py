from abc import ABC, abstractmethod
from typing import List, Tuple
from models.employee import Employee


class BaseReport(ABC):
    def __init__(self, sort_keys: List[Tuple[str, bool]] = None):
        self.sort_keys = sort_keys or []

    def generate(self, employees: List[Employee]) -> None:
        data = self._prepare_data(employees)
        data = self._sort_data(data)
        self._print(data)

    @abstractmethod
    def _prepare_data(self, employees: List[Employee]) -> List[dict]:
        pass

    def _sort_data(self, data: List[dict]) -> List[dict]:
        if not self.sort_keys:
            return data

        for key, reverse in reversed(self.sort_keys):
            data.sort(key=lambda x: x[key], reverse=reverse)
        return data

    @abstractmethod
    def _print(self, data: List[dict]) -> None:
        pass
