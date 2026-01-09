from typing import Dict, Any, List
from botsmith.agents.base_agent import BaseAgent


class WorkflowOptimizerAgent(BaseAgent):
    """
    Optimizes a compiled workflow by reordering and deduplicating steps.
    """

    CANONICAL_ORDER = [
        "analyze_requirements",
        "design_api",
        "define_agents",
        "configure_agents",
        "configure_agents",
        "implement_api",
        "scaffold_project",
        "plan_files",
        "generate_all_files",
        "validate_code",
        "security_scan",
        "optimize_workflow",
        "deployment",
    ]

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        steps: List[Dict[str, Any]] | None = context.get("steps")

        if not steps:
            # If no steps provided, assume we are in a runtime step where context doesn't have them
            # Return no-op success
            return {"status": "skipped", "reason": "No steps to optimize"}

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
