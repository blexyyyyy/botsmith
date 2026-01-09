# botsmith/core/memory/execution_context.py

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class ExecutionContext:
    """
    Formalized ephemeral state for a single agent step.
    Scope: EXECUTION (runtime only, never persisted)
    """
    agent_id: str
    step_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tool_inputs: List[Dict[str, Any]] = field(default_factory=list)
    tool_outputs: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    reasoning_artifacts: List[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_tool_call(self, tool_name: str, inputs: Dict[str, Any], output: Any = None):
        self.tool_inputs.append({"tool": tool_name, "params": inputs})
        if output is not None:
            self.tool_outputs.append({"tool": tool_name, "output": output})

    def add_error(self, error: str):
        self.errors.append(error)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "step_id": self.step_id,
            "tool_inputs": self.tool_inputs,
            "tool_outputs": self.tool_outputs,
            "errors": self.errors,
            "reasoning": self.reasoning_artifacts,
            "metadata": self.metadata,
        }
