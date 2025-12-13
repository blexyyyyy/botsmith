# botsmith/core/utils/logger.py

import logging
from typing import Optional


class Logger:
    """
    Centralized logger factory for the application.
    """

    _configured = False

    @staticmethod
    def _configure_root_logger(level: int = logging.INFO):
        if Logger._configured:
            return

        logging.basicConfig(
            level=level,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
        Logger._configured = True

    @staticmethod
    def get_logger(name: Optional[str] = None) -> logging.Logger:
        Logger._configure_root_logger()
        return logging.getLogger(name if name else "botsmith")
