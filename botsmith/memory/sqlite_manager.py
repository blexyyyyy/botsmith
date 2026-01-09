# botsmith/core/memory/sqlite_manager.py

from typing import Optional, Any
from botsmith.core.memory import AgentMemory, MemoryScope, MemoryUpdateProposal
from botsmith.memory.manager import MemoryManager
from botsmith.persistence.agent_memory_repository import AgentMemoryRepository


class SQLiteMemoryManager(MemoryManager):
    """
    Persistent memory manager backed by SQLite.
    Inherits from the core MemoryManager to provide full 3-layer support.
    """

    def __init__(self, db_path=None, session_id: str = "default_session"):
        self._repo = AgentMemoryRepository(db_path=db_path)
        self._repo.init_schema()
        super().__init__(session_id=session_id, repository=self._repo)
