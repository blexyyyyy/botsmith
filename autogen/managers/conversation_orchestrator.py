# botsmith/autogen/managers/conversation_orchestrator.py

from typing import Dict, Any
from botsmith.core.interfaces.workflow_interface import IWorkflow


class ConversationOrchestrator:
    """
    Executes workflows and manages shared context.
    """

    def __init__(self, workflow: IWorkflow):
        self._workflow = workflow
        self._history: list[Dict[str, Any]] = []

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        result = self._workflow.execute(input_data)
        self._history.append(result)
        return result

    def get_history(self):
        return self._history
