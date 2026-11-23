# Singleton: configuration manager

## Problems in the legacy code (`legacy_config.py`)
- The file is read on **every call** (four reads for one request), which is wasteful and slow I/O.
- There is no shared state: each module gets its own copy.
- Changes are not synchronised: a module that modifies its copy is not seen by the others.
- It's hard to mock in tests because there's no single point to override.

## Design

```mermaid
classDiagram
    class ConfigManager {
        <<singleton>>
        -_instance: ConfigManager$
        -_lock: Lock$
        -_config: dict
        +get_instance(path) ConfigManager$
        +reset()$
        +get(key: str, default) Any
        +set(key: str, value)
    }
    class database { +connect_database() }
    class email_service { +send_email(to, subject) }
    class payment_service { +process_payment(amount) }
    class app { +start_application() }
    database ..> ConfigManager
    email_service ..> ConfigManager
    payment_service ..> ConfigManager
    app ..> ConfigManager
```

- `get_instance()` loads `config.json` on the first call only (lazy initialisation) and returns the same object afterwards.
- `get("database.host")` walks the nested keys.
- `set()` updates the shared instance, so every module sees the change.
- A `threading.Lock` makes the first creation thread-safe. `reset()` exists so tests can start from a clean state.
- Calling `ConfigManager()` directly raises an error, so people must go through `get_instance()`.

```python
config = ConfigManager.get_instance()      # first call: reads the file
config = ConfigManager.get_instance()      # same object, no file read
db_host = config.get("database.host")
```

Run: `python services.py` · `pytest .`
