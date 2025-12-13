from typing import Dict, Any, List
from botsmith.core.base.agent import BaseAgent


class SecurityAgent(BaseAgent):
    """
    Performs security checks on workflow steps.
    """

    DENY_PATTERNS = {
        "rm -rf",
        "shutdown",
        "format",
        "curl | sh",
    }

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        steps: List[Dict[str, Any]] | None = context.get("steps")

        if not steps:
            raise ValueError("No workflow steps provided for security scan")

        violations = []

        for step in steps:
            step_name = step["step"].lower()
            for pattern in self.DENY_PATTERNS:
                if pattern in step_name:
                    violations.append(
                        {"step": step["step"], "issue": f"Forbidden pattern: {pattern}"}
                    )

        return {
            "secure": len(violations) == 0,
            "violations": violations,
        }
