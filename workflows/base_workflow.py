# botsmith/workflows/base_workflow.py

from typing import Dict, Any, List, Callable
from botsmith.core.interfaces.workflow_interface import IWorkflow
from botsmith.core.interfaces.agent_interface import IAgent


class BaseWorkflow(IWorkflow):
    """
    Base class for all workflows.
    """

    def __init__(self, name: str):
        self.name = name
        self._steps: List[tuple[str, Callable]] = []

    def add_step(self, step_name: str, step_fn: Callable):
        self._steps.append((step_name, step_fn))

    def get_workflow_steps(self) -> List[str]:
        return [name for name, _ in self._steps]

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        context = dict(input_data)

        for step_name, step_fn in self._steps:
            context["current_step"] = step_name
            result = step_fn(context)
            context.update(result or {})

        return context
