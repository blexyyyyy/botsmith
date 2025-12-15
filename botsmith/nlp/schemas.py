from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class CommandIntent:
    intent: str
    entities: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    raw_text: str = ""
    ambiguity: Optional[str] = None
