import json
from legacy_reports import LegacyReportGenerator, AnalyticsDashboard
from report_adapter import LegacyReportAdapter, ReportGeneratorInterface, show_report


def test_adapter_implements_target_interface():
    assert isinstance(LegacyReportAdapter(LegacyReportGenerator()), ReportGeneratorInterface)


def test_adapter_converts_xml_to_json_with_types():
    data = {"total_sales": 150000, "orders": 1234, "avg_order": 121.55, "region": "EMEA"}
    out = LegacyReportAdapter(LegacyReportGenerator()).generate(data)
    assert json.loads(out) == data


def test_adapter_really_uses_the_legacy_system(mocker):
    legacy = LegacyReportGenerator()
    spy = mocker.spy(legacy, "generate_report")
    LegacyReportAdapter(legacy).generate({"a": 1})
    spy.assert_called_once_with({"a": 1})


def test_dashboard_receives_json(capsys):
    dashboard = AnalyticsDashboard()
    show_report(LegacyReportAdapter(LegacyReportGenerator()), dashboard, {"orders": 3})
    assert dashboard.last_displayed == {"orders": 3}
    assert "orders: 3" in capsys.readouterr().out
