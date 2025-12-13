import sys
import os
# Add the parent directory of the 'botsmith' folder to sys.path
# This allows 'import botsmith.xxx' to work.
# We need to go up 4 levels: file -> integration -> tests -> botsmith -> Desktop
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.core.memory.manager import InMemoryMemoryManager
from botsmith.core.llm.wrapper import OllamaLLM
import botsmith.agents


def test_executor_agent():
    llm = OllamaLLM()
    mm = InMemoryMemoryManager()
    factory = AgentFactory(llm, mm)

    executor = factory.create_agent({
        "type": "executor",
        "params": {
            "agent_id": "executor_test",
            "agent_type": "logic",
            "capabilities": ["execution"]
        }
    })

    context = {
        "plan": [
            "analyze_requirements",
            "design_api",
            "implement_api",
            "rm -rf /",  # should be skipped
            "deployment",
        ],
        "dry_run": True,
    }

    result = executor.execute("execute plan", context)
    print(result)


if __name__ == "__main__":
    test_executor_agent()
