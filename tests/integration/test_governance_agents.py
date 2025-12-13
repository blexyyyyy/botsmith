import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.core.memory.manager import InMemoryMemoryManager
from botsmith.core.llm.wrapper import OllamaLLM
import botsmith.agents


llm = OllamaLLM()
mm = InMemoryMemoryManager()
factory = AgentFactory(llm, mm)

workflow_steps = [
    {"step": "implement_api"},
    {"step": "analyze_requirements"},
    {"step": "deployment"},
]

context = {
    "steps": workflow_steps,
    "budget": 10.0,
}

optimizer = factory.create_agent({"type": "workflow_optimizer", "params": {"agent_id": "opt"}})
coster = factory.create_agent({"type": "cost_estimator", "params": {"agent_id": "cost"}})
security = factory.create_agent({"type": "security", "params": {"agent_id": "sec"}})

opt_result = optimizer.execute("optimize", context)
context["steps"] = opt_result["optimized_steps"]

print("OPTIMIZED:", opt_result)

print("COST:", coster.execute("estimate", context))
print("SECURITY:", security.execute("scan", context))
