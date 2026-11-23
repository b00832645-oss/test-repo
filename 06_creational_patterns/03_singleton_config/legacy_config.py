"""Starting code from the course exercise (kept for comparison; do not use)."""
import json


def load_config():
    with open("config.json", "r") as f:          # read again on every call
        return json.load(f)


def connect_database():
    config = load_config()
    print(f"Connecting to database at {config['database']['host']}:{config['database']['port']}")


def send_email(to: str, subject: str):
    config = load_config()
    print(f"Sending email from {config['email']['sender']} via {config['email']['smtp_host']}")
