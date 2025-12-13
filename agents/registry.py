# botsmith/agents/registry.py

from typing import Dict, Type
from botsmith.core.interfaces.agent_interface import IAgent


class AgentRegistry:
    """
    Central registry for all agent classes.
    """

    _registry: Dict[str, Type[IAgent]] = {}

    @classmethod
    def register(cls, agent_type: str, agent_class: Type[IAgent]):
        if agent_type in cls._registry:
            raise ValueError(f"Agent type '{agent_type}' already registered")
        cls._registry[agent_type] = agent_class

    @classmethod
    def get(cls, agent_type: str) -> Type[IAgent]:
        if agent_type not in cls._registry:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls._registry[agent_type]

    @classmethod
    def list_available(cls):
        return list(cls._registry.keys())
