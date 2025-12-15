from typing import Dict, Any, List
from botsmith.core.base.agent import BaseAgent
from botsmith.workflows.workflow_factory import WorkflowFactory


class WorkflowCompilerAgent(BaseAgent):
    """
    Compiles plans and routing info into an executable workflow definition.
    Uses WorkflowFactory to generate standard BotSmith step sequences.
    """

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        plan: List[str] | None = context.get("plan")
        route: str | None = context.get("route")
        validation = context.get("validation")

        if not plan or not isinstance(plan, list):
            raise ValueError("No valid plan found for workflow compilation")

        if not route:
            raise ValueError("No route provided for workflow compilation")

        if validation and not validation.get("valid", True):
            raise ValueError("Cannot compile workflow: validation failed")

        # Delegate to WorkflowFactory to build steps
        # We pass None as planner because we already have the plan
        factory = WorkflowFactory(planner_agent=None)
        workflow_steps = factory._build_steps(plan, context)

        return {
            "workflow_name": route,
            "steps": workflow_steps,
            "step_count": len(workflow_steps),
        }
