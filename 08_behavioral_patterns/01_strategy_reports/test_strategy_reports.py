import inspect
import json
import pytest
import strategy_reports as sr
from legacy_report_generator import ReportGenerator as LegacyGenerator

DATA = [{"name": "Sales Q1", "value": 15000}, {"name": "Sales Q2", "value": 18000}]


@pytest.mark.parametrize("strategy, legacy_key", [(sr.PDFFormatStrategy(), "pdf"), (sr.ExcelFormatStrategy(), "excel"),
                                                  (sr.CSVFormatStrategy(), "csv"), (sr.JSONFormatStrategy(), "json")])
def test_same_output_as_legacy(strategy, legacy_key):
    assert sr.ReportGenerator(DATA, strategy).generate_report() == LegacyGenerator(DATA).generate_report(legacy_key)


def test_switch_strategy_at_runtime():
    gen = sr.ReportGenerator(DATA)
    gen.set_strategy(sr.CSVFormatStrategy())
    assert gen.generate_report().startswith("name,value")
    gen.set_strategy(sr.JSONFormatStrategy())
    assert json.loads(gen.generate_report()) == DATA


def test_html_strategy_added_without_editing_context():
    gen = sr.ReportGenerator(DATA, sr.HTMLFormatStrategy())
    assert "<td>Sales Q1</td><td>15000</td>" in gen.generate_report()
    assert "html" not in inspect.getsource(sr.ReportGenerator).lower()   # context never mentions formats


def test_save_uses_strategy_extension(tmp_path):
    gen = sr.ReportGenerator(DATA, sr.CSVFormatStrategy())
    path = gen.save_report(tmp_path / "sales_report")
    assert path.suffix == ".csv" and path.read_text().startswith("name,value")


def test_missing_strategy_raises():
    with pytest.raises(ValueError):
        sr.ReportGenerator(DATA).generate_report()
