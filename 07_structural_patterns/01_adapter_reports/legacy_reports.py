"""Legacy reporting system from the course exercise. Treat it as an external library: don't modify it."""
import json


class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        """Returns XML format - old system."""
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


class AnalyticsDashboard:
    def __init__(self):
        self.last_displayed: dict | None = None

    def display(self, json_data: str):
        data = json.loads(json_data)
        self.last_displayed = data
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")
