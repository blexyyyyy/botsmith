# botsmith/core/interfaces/memory_interface.py

from abc import ABC, abstractmethod
from typing import Optional
from ..memory.models import AgentMemory


class IMemoryManager(ABC):
    """
    Abstraction over agent memory storage.
    Allows swapping in-memory, file-based, DB, or vector memory.
    """

    @abstractmethod
    def save_memory(self, memory: AgentMemory) -> bool:
        """
        Persist agent memory.

        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def load_memory(self, agent_id: str) -> Optional[AgentMemory]:
        """
        Load memory associated with an agent.

        Returns:
            AgentMemory if found, else None
        """
        raise NotImplementedError
