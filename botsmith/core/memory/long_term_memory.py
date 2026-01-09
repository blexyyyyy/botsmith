# botsmith/core/memory/long_term_memory.py

from typing import Any, Dict, Optional
from datetime import datetime
from ..interfaces.memory_store import MemoryStore
from .models import MemoryScope


class PersistentStore(MemoryStore):
    """
    Base class for persistent memories with versioning and confidence tracking.
    """

    def __init__(self, scope: MemoryScope, repository=None):
        self._scope = scope
        self._repository = repository
        self._data: Dict[str, Dict[str, Any]] = {}
        
        if self._repository:
            self._repository.init_schema()
            self._data = self._repository.load_scope(self._scope)

    @property
    def scope(self) -> MemoryScope:
        return self._scope

    def read(self, key: str) -> Any:
        entry = self._data.get(key)
        return entry["value"] if entry else None

    def write(self, key: str, value: Any, meta: Dict[str, Any] = None) -> bool:
        meta = meta or {}
        entry = {
            "value": value,
            "version": meta.get("version", 1),
            "updated_at": datetime.utcnow().isoformat(),
            "source": meta.get("source", "system"),
            "confidence": meta.get("confidence", 1.0)
        }
        self._data[key] = entry
        
        if self._repository:
            self._repository.save_entry(self._scope, key, value, entry)
        return True

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            # Repository delete could be implemented if needed
            return True
        return False

    def snapshot(self) -> Dict[str, Any]:
        return self._data.copy()


class PreferenceMemory(PersistentStore):
    """
    User-scoped persistent memory for preferences (verbosity, tool bias, etc).
    """
    def __init__(self, user_id: str, repository=None):
        super().__init__(MemoryScope.USER, repository)
        self.user_id = user_id


class KnowledgeMemory(PersistentStore):
    """
    Project-scoped persistent memory for confirmed facts and assumptions.
    """
    def __init__(self, project_id: str, repository=None):
        super().__init__(MemoryScope.PROJECT, repository)
        self.project_id = project_id
