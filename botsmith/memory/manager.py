# botsmith/core/memory/manager.py

import json
from typing import Dict, Optional, Any
from botsmith.core.memory import AgentMemory, MemoryScope, MemoryUpdateProposal
from botsmith.memory.memory_policy import MemoryPolicy
from botsmith.memory.session import SessionMemory
from botsmith.memory.long_term import PreferenceMemory, KnowledgeMemory
from botsmith.core.interfaces.memory_interface import IMemoryManager
from botsmith.core.interfaces.memory_store import MemoryStore
from botsmith.persistence.agent_memory_repository import AgentMemoryRepository


class MemoryManager(IMemoryManager):
    """
    Central coordinator for BotSmith memory layers.
    Routes proposals, applies policy, and manages stores.
    """

    def __init__(self, session_id: str = "default_session", repository=None):
        self._repository = repository or AgentMemoryRepository()
        self.session = SessionMemory(session_id)
        self.preference = PreferenceMemory("default_user", repository=self._repository)
        self.knowledge = KnowledgeMemory("default_project", repository=self._repository)
        self.policy = MemoryPolicy()

        self._stores: Dict[MemoryScope, MemoryStore] = {
            MemoryScope.SESSION: self.session,
            MemoryScope.USER: self.preference,
            MemoryScope.PROJECT: self.knowledge
        }

    def get_store(self, scope: MemoryScope) -> MemoryStore:
        return self._stores.get(scope)

    def propose(self, proposal: MemoryUpdateProposal) -> bool:
        """
        Apply policy and route accepted proposals to stores.
        """
        decision = "rejected"
        target_scope = None
        
        if self.policy.validate_proposal(proposal):
            target_scope = self.policy.get_target_scope(proposal)
            store = self._stores.get(target_scope)

            if store:
                meta = {
                    "source": proposal.source,
                    "confidence": proposal.confidence,
                    "justification": proposal.justification,
                    "timestamp": proposal.timestamp.isoformat()
                }
                if store.write(proposal.key, proposal.value, meta):
                    decision = "accepted"

        # STEP 10: Observability (Structured Event)
        event = {
            "event": "memory_update",
            "scope": target_scope.value if target_scope else "none",
            "key": proposal.key,
            "value": proposal.value,
            "source": proposal.source,
            "confidence": proposal.confidence,
            "decision": decision,
            "justification": proposal.justification
        }
        print(f"DEBUG MEMORY EVENT: {json.dumps(event, indent=2)}")
        
        return decision == "accepted"

    def read(self, scope: MemoryScope, key: str) -> Any:
        store = self._stores.get(scope)
        return store.read(key) if store else None

    # Legacy support for existing agents
    def save_memory(self, memory: AgentMemory) -> bool:
        # Map interaction history to SessionMemory for now
        return self.session.write(f"history_{memory.agent_id}", memory.interactions)

    def load_memory(self, agent_id: str) -> Optional[AgentMemory]:
        # Try to reconstruct AgentMemory from stores
        interactions = self.session.read(f"history_{agent_id}") or []
        return AgentMemory(
            agent_id=agent_id,
            interactions=interactions,
            metadata={}
        )
