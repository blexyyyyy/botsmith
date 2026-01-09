import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.memory import MemoryManager
from botsmith.llm.wrapper import OllamaLLM
import botsmith.agents

if __name__ == "__main__":
    llm = OllamaLLM()
    mm = MemoryManager()
    factory = AgentFactory(llm, mm)

    planner = factory.create_agent({
        "type": "planner",
        "params": {
            "agent_id": "planner_1",
            "agent_type": "logic",
            "capabilities": ["planning"]
        }
    })

    print(planner.execute("Build and deploy an API bot", {}))
