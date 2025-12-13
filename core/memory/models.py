# botsmith/core/memory/models.py

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime


@dataclass
class AgentMemory:
    """
    Domain model representing persistent memory for an agent.
    """
    agent_id: str
    interactions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.utcnow)
