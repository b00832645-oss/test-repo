import json
import threading
import pytest
from config_manager import ConfigManager
import services


@pytest.fixture(autouse=True)
def fresh_singleton():
    ConfigManager.reset()
    yield
    ConfigManager.reset()


def test_same_instance_and_single_file_read():
    a = ConfigManager.get_instance()
    b = ConfigManager.get_instance()
    assert a is b
    assert a.load_count == 1


def test_direct_instantiation_is_forbidden():
    with pytest.raises(RuntimeError):
        ConfigManager()


def test_nested_get_and_default():
    config = ConfigManager.get_instance()
    assert config.get("database.host") == "localhost"
    assert config.get("app.debug") is True
    assert config.get("does.not.exist", "fallback") == "fallback"


def test_changes_are_shared_between_modules():
    ConfigManager.get_instance().set("payment.environment", "production")
    assert services.process_payment(10) == "Processing 10€ in production mode"


def test_all_services_read_file_once():
    services.start_application(); services.connect_database()
    services.send_email("a@b.c", "Hi"); services.process_payment(1)
    assert ConfigManager.get_instance().load_count == 1


def test_custom_file_for_tests(tmp_path):
    path = tmp_path / "cfg.json"
    path.write_text(json.dumps({"database": {"host": "test-db"}}))
    assert ConfigManager.get_instance(path).get("database.host") == "test-db"


def test_thread_safe_creation():
    instances = []
    threads = [threading.Thread(target=lambda: instances.append(ConfigManager.get_instance())) for _ in range(20)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert len({id(i) for i in instances}) == 1
