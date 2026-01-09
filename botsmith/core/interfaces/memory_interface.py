# botsmith/core/interfaces/memory_interface.py

from abc import ABC, abstractmethod
from typing import Optional, Any
from ..memory.models import AgentMemory, MemoryScope, MemoryUpdateProposal


class IMemoryManager(ABC):
    """
    Abstraction over agent memory coordination.
    Handles multiple memory layers and policy enforcement.
    """

    @abstractmethod
    def propose(self, proposal: MemoryUpdateProposal) -> bool:
        """
        Propose a memory update. The manager decides if/where to store it.
        """
        raise NotImplementedError

    @abstractmethod
    def read(self, scope: MemoryScope, key: str) -> Any:
        """
        Read a value from a specific memory scope.
        """
        raise NotImplementedError

    @abstractmethod
    def save_memory(self, memory: AgentMemory) -> bool:
        """Persist agent memory (Legacy)."""
        raise NotImplementedError

    @abstractmethod
    def load_memory(self, agent_id: str) -> Optional[AgentMemory]:
        """Load memory associated with an agent (Legacy)."""
        raise NotImplementedError
