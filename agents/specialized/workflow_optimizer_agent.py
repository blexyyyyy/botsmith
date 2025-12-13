from typing import Dict, Any, List
from botsmith.core.base.agent import BaseAgent


class WorkflowOptimizerAgent(BaseAgent):
    """
    Optimizes a compiled workflow by reordering and deduplicating steps.
    """

    CANONICAL_ORDER = [
        "analyze_requirements",
        "design_api",
        "define_agents",
        "configure_agents",
        "implement_api",
        "deployment",
    ]

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        steps: List[Dict[str, Any]] | None = context.get("steps")

        if not steps:
            raise ValueError("No workflow steps provided for optimization")

        step_map = {step["step"]: step for step in steps}

        optimized = []
        for name in self.CANONICAL_ORDER:
            if name in step_map:
                optimized.append(step_map[name])

        return {
            "optimized_steps": optimized,
            "original_count": len(steps),
            "optimized_count": len(optimized),
        }
