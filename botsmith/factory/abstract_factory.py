# botsmith/factory/abstract_factory.py

from abc import ABC, abstractmethod
from typing import Dict, Any
from botsmith.core.interfaces.agent_interface import IAgent


class AbstractAgentFactory(ABC):
    """
    Abstract factory for creating agents from config.
    """

    @abstractmethod
    def create_agent(self, config: Dict[str, Any]) -> IAgent:
        raise NotImplementedError
