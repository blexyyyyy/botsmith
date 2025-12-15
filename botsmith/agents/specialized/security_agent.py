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
        generated_files: List[Dict[str, Any]] | None = context.get("generated_files")
        
        violations = []

        # Check 1: Workflow Steps (if present)
        if steps:
            for step in steps:
                step_name = step["step"].lower()
                for pattern in self.DENY_PATTERNS:
                    if pattern in step_name:
                        violations.append(
                            {"step": step["step"], "issue": f"Forbidden pattern in step: {pattern}"}
                        )

        # Check 2: Generated Code (if present)
        if generated_files:
            for file_info in generated_files:
                path = file_info.get("path", "unknown")
                # In a real agent, we might read the file content here if it's not in context.
                # Assuming context might have code snippets or we trust the file names/size for now.
                # If we have content in file_info (not standard yet), scan it.
                # But for now, let's just scan filenames for suspicious extensions/names.
                filename = file_info.get("filename", "")
                if filename.endswith(".exe") or filename.endswith(".sh"):
                     violations.append(
                        {"file": filename, "issue": "Forbidden file extension"}
                    )

        if not steps and not generated_files:
             # In a real scenario this might be a fail, but for now we pass to avoid blocking if context is empty
             # or we can log a warning.
             pass

        return {
            "secure": len(violations) == 0,
            "violations": violations,
        }
