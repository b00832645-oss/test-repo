"""The four legacy 'modules', now all sharing one ConfigManager instance."""
from config_manager import ConfigManager


def start_application():
    config = ConfigManager.get_instance()
    return f"Starting {config.get('app.name')} (debug={config.get('app.debug')})"


def connect_database():
    config = ConfigManager.get_instance()
    return f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}"


def send_email(to: str, subject: str):
    config = ConfigManager.get_instance()
    return f"Sending '{subject}' to {to} from {config.get('email.sender')} via {config.get('email.smtp_host')}"


def process_payment(amount: float):
    config = ConfigManager.get_instance()
    return f"Processing {amount}€ in {config.get('payment.environment')} mode"


if __name__ == "__main__":
    for line in (start_application(), connect_database(), send_email("user@test.com", "Welcome"),
                 process_payment(99.99)):
        print(line)
    print("config file read", ConfigManager.get_instance().load_count, "time(s)")
