from typing import Dict, Any, TYPE_CHECKING
from botsmith.workflows.workflow_executor import WorkflowExecutor as CoreWorkflowExecutor

if TYPE_CHECKING:
    from botsmith.factory.agent_factory import AgentFactory
    from botsmith.persistence.repository import WorkflowRepository


class WorkflowExecutor:
    """
    Agent wrapper for the core WorkflowExecutor logic.
    Delegates actual execution to botsmith.workflows.workflow_executor.
    """

    def __init__(self, agent_factory: "AgentFactory", repository: "WorkflowRepository"):
        self._agent_factory = agent_factory
        self._repo = repository
        # Instantiate the core executor
        self._core_executor = CoreWorkflowExecutor(agent_factory, repository)

    def execute(self, workflow_def: Dict[str, Any], initial_context: Dict[str, Any]) -> Dict[str, Any]:
        # Delegate execution to the core logic
        # Note: CoreExecutor currently handles logging to list, but maybe not DB persistence per step.
        # If DB persistence is needed, it should be added to CoreWorkflowExecutor or handled here via callbacks.
        # For now, we trust the core executor's logic as provided by the user.
        
        # We wrap it to ensure run_id creation if we want to maintain that table linkage
        run_id = self._repo.create_run(
            workflow_def.get("workflow_name", "unnamed_workflow"), "running"
        )
        
        try:
            result = self._core_executor.execute(workflow_def, initial_context)
            
            status = result.get("status", "success")
            self._repo.update_run_status(run_id, status)
            
            # Map "log" back to context if needed, or just return result
            return result
            
        except Exception as e:
            self._repo.update_run_status(run_id, "failed")
            raise e
