# botsmith/core/memory/models.py

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime

class MemoryScope(Enum):
    EXECUTION = "execution"
    SESSION = "session"
    USER = "user"
    PROJECT = "project"


@dataclass
class AgentMemory:
    """
    Domain model representing persistent memory for an agent.
    """
    agent_id: str
    interactions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MemoryUpdateProposal:
    """
    Proposed update to memory, to be gated by policy.
    """
    key: str
    value: Any
    confidence: float
    justification: str
    suggested_scope: Optional[MemoryScope] = None
    source: str = "agent"
    timestamp: datetime = field(default_factory=datetime.utcnow)
