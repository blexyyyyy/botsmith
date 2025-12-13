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


def test_workflow_compiler_agent():
    llm = OllamaLLM()
    mm = InMemoryMemoryManager()
    factory = AgentFactory(llm, mm)

    compiler = factory.create_agent({
        "type": "workflow_compiler",
        "params": {
            "agent_id": "compiler_test",
            "agent_type": "logic",
            "capabilities": ["workflow_compilation"]
        }
    })

    context = {
        "plan": [
            "analyze_requirements",
            "design_api",
            "implement_api",
            "deployment",
        ],
        "route": "bot_creation_workflow",
        "validation": {"valid": True},
    }

    result = compiler.execute("compile workflow", context)
    print(result)

def test_compiler_invariant():
    llm = OllamaLLM()
    mm = InMemoryMemoryManager()
    factory = AgentFactory(llm, mm)

    compiler = factory.create_agent({
        "type": "workflow_compiler",
        "params": {
            "agent_id": "compiler_invariant_test",
            "agent_type": "logic",
            "capabilities": ["workflow_compilation"]
        }
    })

    context = {
        "plan": ["define_agents", "configure_agents"],
        "route": "bot_creation_workflow",
        "validation": {"valid": True},
    }

    result = compiler.execute("compile workflow", context)
    for step in result["steps"]:
        if step["step"] in ("define_agents", "configure_agents"):
            assert step["agent"] == "planner", f"Step {step['step']} incorrectly mapped to {step['agent']}"

if __name__ == "__main__":
    test_workflow_compiler_agent()
    test_compiler_invariant()
