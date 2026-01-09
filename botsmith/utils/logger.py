# botsmith/core/utils/logger.py

import logging
import json
from typing import Optional, Any
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """
    Structured logging formatter for BotSmith.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        # Add extra context if provided
        if hasattr(record, "run_id"):
            log_data["run_id"] = record.run_id
        if hasattr(record, "workflow_id"):
            log_data["workflow_id"] = record.workflow_id
        if hasattr(record, "agent_name"):
            log_data["agent_name"] = record.agent_name
            
        return json.dumps(log_data)

class Logger:
    """
    Centralized logger factory for the application.
    """

    _configured = False

    @staticmethod
    def _configure_root_logger(level: int = logging.INFO):
        if Logger._configured:
            return

        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        
        root = logging.getLogger()
        root.setLevel(level)
        # Remove existing handlers
        for h in root.handlers[:]:
            root.removeHandler(h)
        root.addHandler(handler)
        
        Logger._configured = True

    @staticmethod
    def get_logger(name: Optional[str] = None) -> logging.Logger:
        Logger._configure_root_logger()
        return logging.getLogger(name if name else "botsmith")
