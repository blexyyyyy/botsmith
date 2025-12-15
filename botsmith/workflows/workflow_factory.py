from typing import Dict, Any, List


from botsmith.core.plugin import PluginManager

class WorkflowFactory:
    """
    Constructs a workflow definition based on the user request and planner output.
    """

    WORKFLOW_NAME = "bot_creation_workflow"

    def __init__(self, planner_agent, plugin_manager: PluginManager = None):
        self.planner = planner_agent
        self.plugin_manager = plugin_manager

    def create_workflow(self, user_request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for creating full workflow.
        """

        # 1. Generate semantic plan (analyze_requirements, define_agents, etc)
        plan_result = self.planner.execute(user_request, context)
        plan = plan_result.get("plan", [])
        context.update(plan_result)

        # 2. Build normalized internal workflow steps
        steps = self._build_steps(plan, context)

        return {
            "workflow_name": self.WORKFLOW_NAME,
            "steps": steps,
            "step_count": len(steps),
        }

    # ------------------------------------------------------------------
    # INTERNAL: convert planner plan -> BotSmith workflow steps
    # ------------------------------------------------------------------
    def _build_steps(self, plan: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        steps = []
        order = 1

        # Universal first step: scaffold project
        steps.append({
            "order": order,
            "step": "scaffold_project",
            "agent": "scaffolder",
            "retry": 1,
            "on_failure": "abort"
        })
        order += 1

        # File planning MUST come before any codegen
        steps.append({
            "order": order,
            "step": "plan_files",
            "agent": "file_planner",
            "retry": 1,
            "on_failure": "abort"
        })
        order += 1

        # Now handle logical steps in planner plan
        for step in plan:
            if step in ("define_agents", "configure_agents", "design_api", "implement_api"):
                steps.append({
                    "order": order,
                    "step": step,
                    "agent": "planner",
                    "retry": 1,
                    "on_failure": "abort"
                })
                order += 1

        # Code generation — but one step per file (resolved at runtime)
        # We insert a placeholder step "generate_all_files"
        steps.append({
            "order": order,
            "step": "generate_all_files",
            "agent": "coder",
            "retry": 1,
            "on_failure": "abort"
        })
        order += 1

        # Validate code
        steps.append({
            "order": order,
            "step": "validate_code",
            "agent": "validator",
            "retry": 1,
            "on_failure": "abort"
        })
        order += 1

        # Security review
        steps.append({
            "order": order,
            "step": "security_scan",
            "agent": "security",
            "retry": 1,
            "on_failure": "abort"
        })
        order += 1

        # Workflow optimization (optional)
        steps.append({
            "order": order,
            "step": "optimize_workflow",
            "agent": "optimizer",
            "retry": 1,
            "on_failure": "continue"
        })
        order += 1

        # Deployment step (final)
        steps.append({
            "order": order,
            "step": "deployment",
            "agent": "executor",
            "retry": 1,
            "on_failure": "abort"
        })

        return steps
