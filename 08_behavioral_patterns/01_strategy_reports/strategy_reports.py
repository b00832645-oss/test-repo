"""Strategy pattern refactoring of the report generator."""
from __future__ import annotations

import html
import json
from abc import ABC, abstractmethod
from pathlib import Path


class FormatStrategy(ABC):
    """Contract shared by every report format."""

    extension: str = ".txt"

    @abstractmethod
    def format(self, data: list[dict]) -> str: ...


class PDFFormatStrategy(FormatStrategy):
    extension = ".pdf"

    def format(self, data):
        lines = ["PDF REPORT", "=" * 50]
        lines += [f"| {item['name']:20} | {item['value']:10} |" for item in data]
        lines += ["=" * 50, "End of PDF Report"]
        return "\n".join(lines)


class ExcelFormatStrategy(FormatStrategy):
    extension = ".xlsx"

    def format(self, data):
        rows = [f"{item['name']}\t{item['value']}" for item in data]
        return "\n".join(["EXCEL REPORT", "-" * 50, "Name\tValue", *rows, "-" * 50]) + "\n"


class CSVFormatStrategy(FormatStrategy):
    extension = ".csv"

    def format(self, data):
        return "name,value\n" + "".join(f"{item['name']},{item['value']}\n" for item in data)


class JSONFormatStrategy(FormatStrategy):
    extension = ".json"

    def format(self, data):
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(FormatStrategy):
    """Added AFTER the refactoring, without touching any other class."""

    extension = ".html"

    def format(self, data):
        rows = "\n".join(f"    <tr><td>{html.escape(str(i['name']))}</td><td>{i['value']}</td></tr>" for i in data)
        return f"<table>\n    <tr><th>Name</th><th>Value</th></tr>\n{rows}\n</table>"


class ReportGenerator:
    """Context: delegates formatting to the current strategy."""

    def __init__(self, data: list[dict], strategy: FormatStrategy | None = None):
        self.data = data
        self._strategy = strategy

    def set_strategy(self, strategy: FormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        if self._strategy is None:
            raise ValueError("No format strategy set: call set_strategy() first")
        return self._strategy.format(self.data)

    def save_report(self, filename: str | Path) -> Path:
        path = Path(f"{filename}{self._strategy.extension}")
        path.write_text(self.generate_report(), encoding="utf-8")
        return path


if __name__ == "__main__":
    data = [{"name": "Sales Q1", "value": 15000}, {"name": "Sales Q2", "value": 18000},
            {"name": "Sales Q3", "value": 22000}, {"name": "Sales Q4", "value": 25000}]
    generator = ReportGenerator(data)
    for strategy in (PDFFormatStrategy(), CSVFormatStrategy(), JSONFormatStrategy(), HTMLFormatStrategy()):
        generator.set_strategy(strategy)              # switch at runtime
        print(f"=== {type(strategy).__name__} ===")
        print(generator.generate_report(), end="\n\n")
