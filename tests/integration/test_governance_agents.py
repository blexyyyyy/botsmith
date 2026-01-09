import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.memory import MemoryManager
from botsmith.llm.wrapper import OllamaLLM
import botsmith.agents


llm = OllamaLLM()
mm = MemoryManager()
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

optimizer = factory.create_agent({"type": "optimizer", "params": {"agent_id": "opt"}})
coster = factory.create_agent({"type": "cost_estimator", "params": {"agent_id": "cost"}})
security = factory.create_agent({"type": "security", "params": {"agent_id": "sec"}})

opt_result = optimizer.execute("optimize", context)
context["steps"] = opt_result["optimized_steps"]

print("OPTIMIZED:", opt_result)

print("COST:", coster.execute("estimate", context))
print("SECURITY:", security.execute("scan", context))
