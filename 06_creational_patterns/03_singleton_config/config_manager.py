"""Singleton configuration manager."""
from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(__file__).with_name("config.json")
_MISSING = object()


class ConfigManager:
    _instance: "ConfigManager | None" = None
    _lock = threading.Lock()
    _creating = False

    def __init__(self, path: Path = DEFAULT_PATH):
        if not ConfigManager._creating:
            raise RuntimeError("Use ConfigManager.get_instance() instead of ConfigManager()")
        self.path = Path(path)
        self.load_count = 0
        self._config: dict = {}
        self._load()

    def _load(self) -> None:
        with open(self.path, encoding="utf-8") as f:
            self._config = json.load(f)
        self.load_count += 1

    @classmethod
    def get_instance(cls, path: Path = DEFAULT_PATH) -> "ConfigManager":
        if cls._instance is None:                  # fast path, no lock once created
            with cls._lock:
                if cls._instance is None:          # double-checked locking
                    cls._creating = True
                    try:
                        cls._instance = cls(path)
                    finally:
                        cls._creating = False
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Forget the instance (used by tests)."""
        with cls._lock:
            cls._instance = None

    def get(self, key: str, default: Any = None) -> Any:
        """Read a nested value with dot notation: get('database.host')."""
        value: Any = self._config
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, key: str, value: Any) -> None:
        """Change a value in the shared configuration (seen by every module)."""
        *parents, last = key.split(".")
        node = self._config
        for part in parents:
            node = node.setdefault(part, {})
        node[last] = value
