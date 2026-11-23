"""Adapter: make the legacy XML report generator usable by the JSON dashboard."""
import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

from legacy_reports import LegacyReportGenerator, AnalyticsDashboard


class ReportGeneratorInterface(ABC):
    """Target interface: what the dashboard expects."""

    @abstractmethod
    def generate(self, data: dict) -> str:
        """Return the report as a JSON string."""


class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy: LegacyReportGenerator):
        self._legacy = legacy                     # adaptee, held by composition

    def generate(self, data: dict) -> str:
        xml = self._legacy.generate_report(data)
        return self._xml_to_json(xml)

    @staticmethod
    def _parse_value(text: str | None):
        if text is None:
            return None
        for cast in (int, float):
            try:
                return cast(text)
            except ValueError:
                pass
        return text

    def _xml_to_json(self, xml: str) -> str:
        root = ET.fromstring(xml)
        return json.dumps({child.tag: self._parse_value(child.text) for child in root})


def show_report(generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard, data: dict) -> None:
    """Business logic no longer knows anything about formats."""
    dashboard.display(generator.generate(data))


if __name__ == "__main__":
    generator = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()
    show_report(generator, dashboard, {"total_sales": 150000, "orders": 1234, "avg_order": 121.55})
    show_report(generator, dashboard, {"total_items": 5000, "low_stock": 45, "out_of_stock": 12})
