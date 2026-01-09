# botsmith/core/memory/memory_policy.py

from typing import Any, Dict, Optional
from .models import MemoryScope, MemoryUpdateProposal


class MemoryPolicy:
    """
    Defines rules that gate all memory writes.
    Ensures architectural authority and prevents hallucinations from becoming permanent.
    """

    def __init__(self):
        self.min_confidence = 0.7

    def validate_proposal(self, proposal: MemoryUpdateProposal) -> bool:
        """
        Evaluate if a memory update proposal should be accepted.
        """
        # Rule 1: Confidence score threshold
        if proposal.confidence < self.min_confidence:
            return False

        # Rule 2: Scope-based restrictions
        if proposal.suggested_scope == MemoryScope.USER:
            # Agents cannot overwrite user preferences directly
            if proposal.source.startswith("agent"):
                return False

        # Rule 3: Project Knowledge rules
        if proposal.suggested_scope == MemoryScope.PROJECT:
            # Knowledge requires even higher confidence if from agent
            if proposal.source.startswith("agent") and proposal.confidence < 0.9:
                return False

        return True

    def get_target_scope(self, proposal: MemoryUpdateProposal) -> MemoryScope:
        """
        Decide the final storage scope for a proposal.
        """
        if proposal.suggested_scope:
            return proposal.suggested_scope
        
        # Default heuristic
        if proposal.source.startswith("agent"):
            return MemoryScope.SESSION
        
        return MemoryScope.EXECUTION
