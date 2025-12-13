# botsmith/core/interfaces/workflow_interface.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IWorkflow(ABC):
    """
    Contract for orchestrating multi-step agent interactions.
    """

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the workflow.

        Args:
            input_data: Initial data required to start the workflow

        Returns:
            Final aggregated result
        """
        raise NotImplementedError

    @abstractmethod
    def get_workflow_steps(self) -> List[str]:
        """
        Return ordered list of workflow step names.
        Used for introspection and debugging.
        """
        raise NotImplementedError
