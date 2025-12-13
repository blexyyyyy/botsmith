from typing import Dict, Any, List
from botsmith.core.base.agent import BaseAgent


class ExecutorAgent(BaseAgent):
    """
    Deterministic executor agent.
    Executes approved actions based on a plan.
    """

    ALLOWED_ACTIONS = {
        "analyze_requirements",
        "design_api",
        "implement_api",
        "define_agents",
        "configure_agents",
        "deployment",
    }

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Guardrail: Planning must occur before execution
        if isinstance(context.get("plan"), list):
            raise RuntimeError(
                "ExecutorAgent received a plan. Planning must occur before execution."
            )

        dry_run = context.get("dry_run", True)

        try:
            result = self._execute_step(task, dry_run=dry_run)
            return {
                "executed": [{"step": task, "result": result, "dry_run": dry_run}],
                "skipped": [],
                "errors": [],
                "dry_run": dry_run,
                "status": "success",
            }
        except Exception as e:
            return {
                "executed": [],
                "skipped": [],
                "errors": [{"step": task, "error": str(e)}],
                "dry_run": dry_run,
                "status": "failed",
            }

    def _execute_step(self, step: str, dry_run: bool) -> str:
        """
        Executes a single step.
        """
        if dry_run:
            return f"[DRY RUN] {step} simulated"

        # Real execution hooks go here
        # For now, we simulate safely
        return f"{step} executed successfully"
