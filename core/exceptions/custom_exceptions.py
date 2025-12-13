# botsmith/core/exceptions/custom_exceptions.py

class BotSmithError(Exception):
    """Base exception for all BotSmith-related errors."""
    pass


class ConfigurationError(BotSmithError):
    """Raised when configuration is invalid or missing."""
    pass


class LLMUnavailableError(BotSmithError):
    """Raised when the LLM backend is not reachable."""
    pass


class AgentExecutionError(BotSmithError):
    """Raised when an agent fails during execution."""
    pass


class WorkflowExecutionError(BotSmithError):
    """Raised when a workflow fails to complete."""
    pass
