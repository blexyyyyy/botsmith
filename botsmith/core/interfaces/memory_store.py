# botsmith/core/interfaces/memory_store.py

from abc import ABC, abstractmethod
from typing import Any, Dict
from ..memory.models import MemoryScope


class MemoryStore(ABC):
    """
    Universal interface for all persistent or semi-persistent memory stores.
    """
    
    @property
    @abstractmethod
    def scope(self) -> MemoryScope:
        """The scope this store operates in."""
        pass

    @abstractmethod
    def read(self, key: str) -> Any:
        """Read a value from the store."""
        pass

    @abstractmethod
    def write(self, key: str, value: Any, meta: Dict[str, Any] = None) -> bool:
        """Write a value to the store with optional metadata."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a key from the store."""
        pass

    @abstractmethod
    def snapshot(self) -> Dict[str, Any]:
        """Return a full snapshot of the store's current state."""
        pass
