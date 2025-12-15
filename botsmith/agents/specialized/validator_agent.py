from typing import Dict, Any
from botsmith.core.base.agent import BaseAgent


class ValidatorAgent(BaseAgent):
    """
    Deterministic validator agent.
    Enforces structure and logical constraints.
    """

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Expecting a plan in context
        plan = context.get("plan")

        if not plan or not isinstance(plan, list):
            raise ValueError("No valid plan found in context")
            
        plan_set = set(plan)
        errors = []

        # Rule 1: Must have analysis
        if "analyze_requirements" not in plan_set:
            errors.append("Missing required step: analyze_requirements")
            
        # Rule 2: Must have implementation phase (either API or Agent definition)
        if not ("implement_api" in plan_set or "define_agents" in plan_set):
             errors.append("Missing implementation phase (implement_api OR define_agents)")

        if errors:
            return {
                "valid": False,
                "errors": errors,
            }

        return {
            "valid": True,
            "message": "Plan passed all validation checks",
        }
