import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from botsmith.memory import SQLiteMemoryManager
from botsmith.factory.agent_factory import AgentFactory
from botsmith.llm import OllamaLLM
import botsmith.agents
from botsmith.persistence.database import init_db


def test_agent_memory_persists_across_instances():
    init_db()
    llm = OllamaLLM()

    mm1 = SQLiteMemoryManager()
    factory1 = AgentFactory(llm, mm1)

    agent1 = factory1.create_agent({
        "type": "planner",
        "params": {
            "agent_id": "memory_test_agent",
            "agent_type": "logic",
            "capabilities": [],
        },
    })

    import traceback
    try:
        agent1.execute("test task", {})
    except Exception:
        # Expected failure, but memory should propagate
        pass
    del agent1

    mm2 = SQLiteMemoryManager()
    factory2 = AgentFactory(llm, mm2)

    agent2 = factory2.create_agent({
        "type": "planner",
        "params": {
            "agent_id": "memory_test_agent",
            "agent_type": "logic",
            "capabilities": [],
        },
    })


    # STEP 2.3: Assert Against Project Memory via MemoryManager
    from botsmith.core.memory import MemoryScope
    
    project_store = mm2.get_store(MemoryScope.PROJECT)
    interaction = project_store.read("interaction_1")
    
    assert interaction is not None
    assert interaction["task"] == "test task"
    print("Test Passed!")

if __name__ == "__main__":
    test_agent_memory_persists_across_instances()
