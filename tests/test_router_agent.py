import sys
import os
# Add the parent directory of the 'botsmith' folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.core.memory.manager import InMemoryMemoryManager
from botsmith.core.llm.wrapper import OllamaLLM
import botsmith.agents


def test_router_agent():
    # Helper to print steps
    print("Initializing components...")
    try:
        # Use real Ollama LLM
        llm = OllamaLLM()
        mm = InMemoryMemoryManager()
        factory = AgentFactory(llm, mm)

        print("Creating Router Agent...")
        router = factory.create_agent({
            "type": "router",
            "params": {
                "agent_id": "router_test",
                "agent_type": "logic",
                "capabilities": ["routing"]
            }
        })
        print(f"Agent Created: {router}")

        # Test 1: Rule-based
        test_task_1 = "Build a bot that scrapes jobs"
        print(f"Executing routing for task 1: '{test_task_1}'")
        result_1 = router.execute(test_task_1, {})
        print("Result 1:", result_1)
        
        expected_route_1 = "bot_creation_workflow"
        if result_1.get("route") == expected_route_1:
            print("Test 1 PASSED: Rule-based route identified.")
        else:
            print(f"Test 1 FAILED: Expected {expected_route_1}, got {result_1.get('route')}")
            
        # Test 2: NLP fallback
        # "Analyze this project" doesn't match basic substrings for "analyze" in the original simple router? 
        # Wait, the original router didn't have "analyze" in its hardcoded rules, only "build bot", "api", "deploy".
        # So this should hit NLP.
        test_task_2 = "Please analyze this project structure"
        print(f"Executing routing for task 2: '{test_task_2}'")
        result_2 = router.execute(test_task_2, {})
        print("Result 2:", result_2)
        
        # We mapped "analyze" intent to "analysis_workflow" in the fallback map
        expected_route_2 = "analysis_workflow"
        if result_2.get("route") == expected_route_2:
            print("Test 2 PASSED: NLP fallback route identified.")
        else:
            print(f"Test 2 FAILED: Expected {expected_route_2}, got {result_2.get('route')}")

    except Exception as e:
        print(f"Test FAILED with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_router_agent()
