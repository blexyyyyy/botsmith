from typing import Dict, Any
from botsmith.core.base.agent import BaseAgent
from botsmith.agents.specialized.nlp_interpreter_agent import NLPInterpreterAgent


class RouterAgent(BaseAgent):
    """
    Deterministic router agent.
    Decides which workflow or execution path to take.
    """

    def __init__(self, llm, memory_manager, **kwargs):
        # Ensure we pass all required args to BaseAgent
        super().__init__(
            llm=llm,
            memory_manager=memory_manager,
            **kwargs
        )
        # Instantiate NLP agent internally with its own identity
        self._nlp = NLPInterpreterAgent(
            llm=llm,
            memory_manager=memory_manager,
            agent_id=f"{kwargs.get('agent_id', 'router')}_nlp",
            agent_type="nlp_interpreter",
            capabilities=["semantic_parsing"]
        )

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        task_lower = task.lower()

        # 1. Quick rule-based routing
        route = "unknown"

        if "build" in task_lower and "bot" in task_lower:
            route = "bot_creation_workflow"
        elif "api" in task_lower:
            route = "api_workflow"
        elif "deploy" in task_lower:
            route = "deployment_workflow"
        elif context.get("plan"):
            route = "plan_execution_workflow"

        # 2. If rules fail (unknown), fallback to NLP
        if route == "unknown":
            nlp_result = self._nlp.execute(task, context)
            intent = nlp_result.get("intent", "unknown")
            
            # Map intents to workflows
            intent_map = {
                "build_bot": "bot_creation_workflow",
                "deploy": "deployment_workflow",
                "analyze": "analysis_workflow",
            }
            
            route = intent_map.get(intent, "unknown")
            
            if route != "unknown":
                return {
                    "route": route,
                    "reason": f"NLP matched intent: {intent}",
                    "nlp_info": nlp_result
                }

        if route == "unknown":
            raise ValueError("Unable to determine execution route")

        return {
            "route": route,
            "reason": "Matched routing rules successfully",
        }
    