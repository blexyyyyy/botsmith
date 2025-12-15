import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from botsmith.core.memory.sqlite_manager import SQLiteMemoryManager
from botsmith.factory.agent_factory import AgentFactory
from botsmith.core.llm.wrapper import OllamaLLM
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


    memory = agent2._memory
    assert len(memory.interactions) > 0
    print("Test Passed!")

if __name__ == "__main__":
    test_agent_memory_persists_across_instances()
