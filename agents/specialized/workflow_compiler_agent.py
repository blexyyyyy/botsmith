from typing import Dict, Any, List
from botsmith.core.base.agent import BaseAgent


class WorkflowCompilerAgent(BaseAgent):
    """
    Compiles plans and routing info into an executable workflow definition.
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

        workflow = self._compile(plan, route)

        return {
            "workflow_name": route,
            "steps": workflow,
            "step_count": len(workflow),
        }

    def _compile(self, plan: List[str], route: str) -> List[Dict[str, Any]]:
        """
        Converts a plan into an ordered workflow definition.
        """

        compiled_steps = []

        for idx, step in enumerate(plan):
            compiled_steps.append(
                {
                    "order": idx + 1,
                    "step": step,
                    "agent": self._resolve_agent(step),
                    "retry": 1,
                    "on_failure": "abort",
                }
            )

        return compiled_steps

    def _resolve_agent(self, step: str) -> str:
        """
        Maps a step to an agent type.
        """
        mapping = {
            "analyze_requirements": "executor",
            "design_api": "code_generator",
            "implement_api": "code_generator",
            "define_agents": "planner",
            "configure_agents": "planner",
            "deployment": "executor",
        }

        return mapping.get(step, "executor")
