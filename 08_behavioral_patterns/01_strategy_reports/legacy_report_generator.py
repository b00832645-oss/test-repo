"""Starting code from the course exercise (kept for comparison; do not use)."""
import json


class ReportGenerator:
    def __init__(self, data):
        self.data = data

    def generate_report(self, format_type):
        if format_type == "pdf":
            report = "PDF REPORT\n" + "=" * 50 + "\n"
            for item in self.data:
                report += f"| {item['name']:20} | {item['value']:10} |\n"
            return report + "=" * 50 + "\n" + "End of PDF Report"
        elif format_type == "excel":
            report = "EXCEL REPORT\n" + "-" * 50 + "\n" + "Name\tValue\n"
            for item in self.data:
                report += f"{item['name']}\t{item['value']}\n"
            return report + "-" * 50 + "\n"
        elif format_type == "csv":
            report = "name,value\n"
            for item in self.data:
                report += f"{item['name']},{item['value']}\n"
            return report
        elif format_type == "json":
            return json.dumps(self.data, indent=2)
        else:
            return "Unknown format"
