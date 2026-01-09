# botsmith/core/utils/config_loader.py

import importlib.util
from pathlib import Path
from typing import Any
from botsmith.core.exceptions.custom_exceptions import ConfigurationError


class ConfigLoader:
    """
    Loads configuration from a Python file.
    """

    @staticmethod
    def load(config_path: str) -> Any:
        path = Path(config_path)

        if not path.exists():
            raise ConfigurationError(f"Config file not found: {config_path}")

        spec = importlib.util.spec_from_file_location("botsmith_config", path)
        if spec is None or spec.loader is None:
            raise ConfigurationError(f"Unable to load config: {config_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
