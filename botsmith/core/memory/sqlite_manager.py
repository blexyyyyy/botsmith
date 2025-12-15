from typing import Optional
from datetime import datetime

from botsmith.core.interfaces.memory_interface import IMemoryManager
from botsmith.core.memory.models import AgentMemory
from botsmith.persistence.agent_memory_repository import AgentMemoryRepository


class SQLiteMemoryManager(IMemoryManager):
    """
    Persistent memory manager backed by SQLite.
    """

    def __init__(self, db_path=None):
        self._repo = AgentMemoryRepository(db_path=db_path)
        self._repo.init_schema()

    def load_memory(self, agent_id: str) -> Optional[AgentMemory]:
        return self._repo.load(agent_id)

    def save_memory(self, memory: AgentMemory) -> bool:
        memory.last_updated = datetime.utcnow()
        self._repo.save(memory)
        return True
