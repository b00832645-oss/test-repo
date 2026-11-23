"""Starting code from the course exercise, shortened (kept for comparison; do not use).
CSVPipeline, APIPipeline and DatabasePipeline each repeat this whole run() method."""


class CSVPipeline:
    def __init__(self, source):
        self.source = source
        self.data = None

    def run(self):
        print(f"Connecting to CSV file: {self.source}")
        self.data = [{"id": 1, "name": "Alice", "age": 30}, {"id": 2, "name": "Bob", "age": 25}]
        for record in self.data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()
        for record in self.data:                      # validation: duplicated in every class
            if "id" not in record or "name" not in record:
                raise ValueError("Invalid record structure")
        print(f"Loaded {len(self.data)} records successfully")
        self.data = None                              # cleanup: duplicated in every class
        return "CSV Pipeline finished"
