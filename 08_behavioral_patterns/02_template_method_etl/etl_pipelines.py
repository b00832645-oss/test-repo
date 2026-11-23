"""Template Method refactoring of the ETL pipelines."""
from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class DataPipeline(ABC):
    """Defines the ETL workflow once; subclasses fill in the specific steps."""

    simulated_latency = 0.0          # set > 0 to mimic slow I/O (tests keep it at 0)

    def __init__(self, source: str):
        self.source = source
        self.data: list[dict] | None = None
        self.log: list[str] = []

    # ---- the template method: do NOT override --------------------------------
    def run(self) -> str:
        self.before_step("connect")
        self.connect()

        self.before_step("extract")
        self.data = self.extract()
        self._say(f"Extracted {len(self.data)} records")

        self.before_step("transform")
        self.data = self.transform(self.data)

        self.before_step("validate")
        if self.should_validate():          # hook
            self.validate(self.data)

        self.before_step("load")
        self.load(self.data)

        self.before_step("cleanup")
        self.cleanup()
        return f"{self.label} Pipeline finished"

    # ---- abstract steps: MUST be implemented --------------------------------------
    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def extract(self) -> list[dict]: ...

    @abstractmethod
    def transform(self, data: list[dict]) -> list[dict]: ...

    @abstractmethod
    def required_fields(self) -> tuple[str, ...]: ...

    # ---- shared steps: written once -------------------------------------------------
    @property
    def label(self) -> str:
        return type(self).__name__.replace("Pipeline", "")

    def validate(self, data: list[dict]) -> None:
        for record in data:
            missing = [f for f in self.required_fields() if f not in record]
            if missing:
                raise ValueError(f"Invalid record structure: missing {missing}")
        self._say("Validation passed")

    def load(self, data: list[dict]) -> None:
        time.sleep(self.simulated_latency)
        self._say(f"Loaded {len(data)} records successfully")

    def cleanup(self) -> None:
        self.data = None
        self._say("Cleanup complete")

    # ---- hooks: optional, with defaults -----------------------------------------------
    def should_validate(self) -> bool:
        return True

    def before_step(self, step_name: str) -> None:
        """Logging hook: empty by default."""

    def _say(self, message: str) -> None:
        self.log.append(message)
        print(message)


class CSVPipeline(DataPipeline):
    def connect(self):
        self._say(f"Connecting to CSV file: {self.source}")

    def extract(self):
        return [{"id": 1, "name": "Alice", "age": "30"}, {"id": 2, "name": "Bob", "age": "25"}]

    def transform(self, data):
        return [{**r, "age": int(r["age"]), "name": r["name"].upper()} for r in data]

    def required_fields(self):
        return ("id", "name")


class APIPipeline(DataPipeline):
    def connect(self):
        self._say(f"Connecting to API: {self.source}")

    def extract(self):
        return [{"user_id": 101, "username": "Charlie", "score": "85"},
                {"user_id": 102, "username": "Diana", "score": "92"}]

    def transform(self, data):
        out = []
        for r in data:
            score = int(r["score"])
            out.append({**r, "score": score, "username": r["username"].lower(), "grade": "A" if score >= 90 else "B"})
        return out

    def required_fields(self):
        return ("user_id", "username")


class DatabasePipeline(DataPipeline):
    def connect(self):
        self._say(f"Connecting to database: {self.source}")

    def extract(self):
        return [{"product_id": 501, "product_name": "laptop", "price": "1200"},
                {"product_id": 502, "product_name": "mouse", "price": "25"}]

    def transform(self, data):
        out = []
        for r in data:
            price = float(r["price"])
            out.append({**r, "price": price, "product_name": r["product_name"].title(), "tax": price * 0.2})
        return out

    def required_fields(self):
        return ("product_id", "price")


class XMLPipeline(DataPipeline):
    """New pipeline added to validate the design: only the specific parts are written."""

    SAMPLE = """<orders>
        <order id="9001"><customer>Eve</customer><amount>49.90</amount></order>
        <order id="9002"><customer>Frank</customer><amount>120.00</amount></order>
    </orders>"""

    def connect(self):
        self._say(f"Opening XML file: {self.source}")

    def extract(self):
        root = ET.fromstring(self.SAMPLE)
        return [{"order_id": o.get("id"), "customer": o.findtext("customer"), "amount": o.findtext("amount")}
                for o in root.findall("order")]

    def transform(self, data):
        return [{**r, "order_id": int(r["order_id"]), "amount": float(r["amount"])} for r in data]

    def required_fields(self):
        return ("order_id", "amount")


class QuickCSVPipeline(CSVPipeline):
    """Example of a hook override: skip validation for trusted internal files."""

    def should_validate(self):
        return False


if __name__ == "__main__":
    for pipeline in (CSVPipeline("data/users.csv"), APIPipeline("https://api.example.com/users"),
                     DatabasePipeline("postgresql://localhost/mydb"), XMLPipeline("data/orders.xml")):
        print(f"\nRUNNING {pipeline.label.upper()} PIPELINE\n" + "=" * 40)
        print(pipeline.run())
