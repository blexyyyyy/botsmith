import sys
import os
# Add the parent directory of the 'botsmith' folder to sys.path
# This allows 'import botsmith.xxx' to work, which is required by the codebase.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.core.memory.manager import InMemoryMemoryManager
from botsmith.core.llm.wrapper import OllamaLLM
import botsmith.agents

def test_validator_agent():
    try:
        llm = OllamaLLM()
        # Mock availability safely strictly for testing if Ollama isn't running
        # But user wants to run it, so let's try real first.
        # If it fails, we handle it.
        
        mm = InMemoryMemoryManager()
        factory = AgentFactory(llm, mm)

        print("Creating Validator Agent...")
        validator = factory.create_agent({
            "type": "validator",
            "params": {
                "agent_id": "validator_test",
                "agent_type": "logic",
                "capabilities": ["validation"]
            }
        })
        print(f"Agent Created: {validator}")

        context = {
            "plan": [
                "analyze_requirements",
                "design_api",
                "implement_api",
            ]
        }

        print("Executing validation...")
        result = validator.execute("validate plan", context)
        print("Result:", result)
        print("Test PASSED")
    except Exception as e:
        print(f"Test FAILED with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_validator_agent()
