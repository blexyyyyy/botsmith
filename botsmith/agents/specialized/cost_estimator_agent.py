from typing import Dict, Any, List
from botsmith.core.base.agent import BaseAgent


class CostEstimatorAgent(BaseAgent):
    """
    Estimates cost of a compiled workflow before execution.
    """

    COST_PER_STEP = {
        "analyze_requirements": 1.0,
        "design_api": 2.0,
        "implement_api": 5.0,
        "define_agents": 1.5,
        "configure_agents": 1.5,
        "deployment": 3.0,
    }

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        steps: List[Dict[str, Any]] | None = context.get("steps")
        budget = context.get("budget", 10.0)

        if not steps:
            raise ValueError("No workflow steps provided for cost estimation")

        total_cost = 0.0
        breakdown = []

        for step in steps:
            step_name = step["step"]
            cost = self.COST_PER_STEP.get(step_name, 1.0)
            total_cost += cost
            breakdown.append({"step": step_name, "cost": cost})

        approved = total_cost <= budget

        return {
            "estimated_cost": total_cost,
            "budget": budget,
            "approved": approved,
            "breakdown": breakdown,
        }
