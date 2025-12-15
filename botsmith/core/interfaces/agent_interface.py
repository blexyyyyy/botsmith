# botsmith/core/interfaces/agent_interface.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IAgent(ABC):
    """
    Contract for all agents in the system.
    An agent takes a task + context and produces a structured result.
    """

    @abstractmethod
    def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task using the given context.

        Args:
            task: Natural language or structured task description
            context: Shared state, prior outputs, or configuration

        Returns:
            Dict containing result, metadata, and status
        """
        raise NotImplementedError

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return a list of capabilities this agent supports.
        Used for discovery, routing, and validation.
        """
        raise NotImplementedError

    @abstractmethod
    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Return performance metrics such as success rate, latency, or cost.
        """
        raise NotImplementedError
