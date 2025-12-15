# botsmith/core/memory/manager.py

from typing import Dict, Optional
from .models import AgentMemory
from ..interfaces.memory_interface import IMemoryManager


class InMemoryMemoryManager(IMemoryManager):
    """
    In-memory implementation of IMemoryManager.

    Intended for:
    - local development
    - testing
    - deterministic behavior

    NOT intended for production persistence.
    """

    def __init__(self):
        self._store: Dict[str, AgentMemory] = {}

    def save_memory(self, memory: AgentMemory) -> bool:
        self._store[memory.agent_id] = memory
        return True

    def load_memory(self, agent_id: str) -> Optional[AgentMemory]:
        return self._store.get(agent_id)
