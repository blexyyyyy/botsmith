from typing import Dict, Any, List
from botsmith.core.base.agent import BaseAgent


class PlannerAgent(BaseAgent):
    """
    Deterministic agent that converts intent into an execution plan.
    """

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        task_lower = task.lower()

        plan = []

        # Hard rules (this is the power)
        if "api" in task_lower:
            plan.extend(["analyze_requirements", "design_api", "implement_api"])

        if "bot" in task_lower or "agent" in task_lower:
            plan.extend([
        "analyze_requirements",
        "define_agents",
        "configure_agents",
        "scaffold_project",
    ])

        if "deploy" in task_lower:
            plan.append("deployment")

        if not plan:
            raise ValueError("Unable to derive plan from task")

        # Enforce order & uniqueness
        plan = self._normalize_plan(plan)

        return {
            "plan": plan,
            "confidence": "high",
        }

    def _normalize_plan(self, steps: List[str]) -> List[str]:
        seen = set()
        ordered = []

        for step in steps:
            if step not in seen:
                seen.add(step)
                ordered.append(step)

        return ordered
