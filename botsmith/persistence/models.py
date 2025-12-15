from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class WorkflowRun:
    workflow_name: str
    status: str


@dataclass
class WorkflowStepResult:
    run_id: int
    step_name: str
    agent: str
    status: str
    output: str


@dataclass
class AgentRecord:
    agent_id: str
    agent_type: str
    capabilities: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
