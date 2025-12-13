from typing import Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from botsmith.factory.agent_factory import AgentFactory
    from botsmith.persistence.repository import WorkflowRepository
from botsmith.persistence.models import WorkflowStepResult


class WorkflowExecutor:
    """
    Executes a compiled workflow definition step by step.
    """

    def __init__(self, agent_factory: "AgentFactory", repository: "WorkflowRepository"):
        self._agent_factory = agent_factory
        self._repo = repository

    def execute(self, workflow_def: Dict[str, Any], initial_context: Dict[str, Any]) -> Dict[str, Any]:
        run_id = self._repo.create_run(
            workflow_def.get("workflow_name", "unnamed_workflow"), "running"
        )
        steps: List[Dict[str, Any]] = workflow_def.get("steps", [])
        context = dict(initial_context)

        execution_log = []

        for step_def in steps:
            agent_type = step_def["agent"]
            step_name = step_def["step"]
            retries = step_def.get("retry", 1)
            on_failure = step_def.get("on_failure", "abort")

            attempt = 0
            success = False
            last_error = None

            while attempt < retries and not success:
                attempt += 1
                try:
                    agent = self._agent_factory.create_agent({
                        "type": agent_type,
                        "params": {
                            "agent_id": f"{agent_type}_{step_name}",
                            "agent_type": "logic",
                            "capabilities": [step_name],
                        },
                    })

                    agent_context = context.copy()
                    # Guardrail: Ensure executor doesn't see the raw plan to prevent double execution
                    if agent_type == "executor" and "plan" in agent_context:
                        del agent_context["plan"]

                    result = agent.execute(step_name, agent_context)
                    context.update(result if isinstance(result, dict) else {})
                    execution_log.append({
                        "step": step_name,
                        "agent": agent_type,
                        "status": "success",
                        "attempt": attempt,
                        "result": result,
                    })
                    success = True
                    self._repo.save_step(
                        WorkflowStepResult(
                            run_id=run_id,
                            step_name=step_name,
                            agent=agent_type,
                            status="success",
                            output=str(result),
                        )
                    )

                except Exception as e:
                    last_error = str(e)
                    execution_log.append({
                        "step": step_name,
                        "agent": agent_type,
                        "status": "failed",
                        "attempt": attempt,
                        "error": last_error,
                    })
                    self._repo.save_step(
                        WorkflowStepResult(
                            run_id=run_id,
                            step_name=step_name,
                            agent=agent_type,
                            status="failed",
                            output=str(last_error),
                        )
                    )

            if not success:
                if on_failure == "abort":
                    return {
                        "status": "failed",
                        "failed_step": step_name,
                        "error": last_error,
                        "log": execution_log,
                    }
                
                self._repo.update_run_status(run_id, "failed")
                return {
                    "status": "failed",
                    "failed_step": step_name,
                    "error": last_error,
                    "log": execution_log,
                }

        self._repo.update_run_status(run_id, "success")
        return {
            "status": "success",
            "log": execution_log,
            "final_context": context,
        }
