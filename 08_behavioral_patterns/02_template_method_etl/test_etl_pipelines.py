import pytest
from etl_pipelines import (DataPipeline, CSVPipeline, APIPipeline, DatabasePipeline, XMLPipeline,
                           QuickCSVPipeline)


@pytest.mark.parametrize("cls, label", [(CSVPipeline, "CSV"), (APIPipeline, "API"),
                                        (DatabasePipeline, "Database"), (XMLPipeline, "XML")])
def test_every_pipeline_runs(cls, label):
    assert cls("src").run() == f"{label} Pipeline finished"


def test_steps_always_run_in_order():
    calls = []

    class Spy(CSVPipeline):
        def before_step(self, name):
            calls.append(name)

    Spy("x").run()
    assert calls == ["connect", "extract", "transform", "validate", "load", "cleanup"]


def test_transformations():
    p = APIPipeline("x")
    data = p.transform(p.extract())
    assert [r["grade"] for r in data] == ["B", "A"] and data[0]["username"] == "charlie"
    db = DatabasePipeline("x")
    assert db.transform(db.extract())[0] == {"product_id": 501, "product_name": "Laptop", "price": 1200.0, "tax": 240.0}


def test_xml_pipeline_parses_xml():
    p = XMLPipeline("x")
    assert p.transform(p.extract()) == [{"order_id": 9001, "customer": "Eve", "amount": 49.9},
                                        {"order_id": 9002, "customer": "Frank", "amount": 120.0}]


def test_shared_validation_rejects_bad_records():
    class Broken(CSVPipeline):
        def extract(self):
            return [{"name": "no id", "age": "1"}]

    with pytest.raises(ValueError, match="missing"):
        Broken("x").run()


def test_hook_can_skip_validation():
    p = QuickCSVPipeline("x")
    p.run()
    assert "Validation passed" not in p.log


def test_cleanup_always_runs():
    p = CSVPipeline("x")
    p.run()
    assert p.data is None and p.log[-1] == "Cleanup complete"


def test_base_class_is_abstract():
    with pytest.raises(TypeError):
        DataPipeline("x")
