import json
import os
import sys

# Ensure project root is in path (add parent of botsmith folder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.memory import MemoryManager
from botsmith.llm.wrapper import OllamaLLM
import botsmith.agents  # forces registration
from botsmith.agents.registry import AgentRegistry # explicit import to check

def test_factory():
    print("Filesystem path:", os.getcwd())
    # Resolve config path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))
    config_path = os.path.join(project_root, "botsmith/config/agent_configs.json")
    print("Loading config from:", config_path)
    
    with open(config_path) as f:
        cfg = json.load(f)

    llm = OllamaLLM()
    mm = MemoryManager()

    factory = AgentFactory(local_llm=llm, memory_manager=mm)

    print(f"Creating agent of type: {cfg['agents'][0]['type']}")
    agent = factory.create_agent(cfg["agents"][0])
    
    print("Executing agent...")
    result = agent.execute("Say hello in one sentence.", {})
    print("Result:", result)

if __name__ == "__main__":
    test_factory()
