# botsmith/core/memory/session_memory.py

from typing import Any, Dict
from ..interfaces.memory_store import MemoryStore
from .models import MemoryScope


class SessionMemory(MemoryStore):
    """
    Workflow-scoped memory shared across agents in a single run.
    Scope: SESSION
    """

    def __init__(self, session_id: str):
        self._session_id = session_id
        self._data: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    @property
    def scope(self) -> MemoryScope:
        return MemoryScope.SESSION

    def read(self, key: str) -> Any:
        return self._data.get(key)

    def write(self, key: str, value: Any, meta: Dict[str, Any] = None) -> bool:
        self._data[key] = value
        if meta:
            self._metadata[key] = meta
        return True

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            self._metadata.pop(key, None)
            return True
        return False

    def snapshot(self) -> Dict[str, Any]:
        return {
            "session_id": self._session_id,
            "data": self._data.copy(),
            "metadata": self._metadata.copy()
        }
