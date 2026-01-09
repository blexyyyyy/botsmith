import sys
import os
# Add the parent directory of the 'botsmith' folder to sys.path
# This allows 'import botsmith.xxx' to work.
# We need to go up 4 levels: file -> integration -> tests -> botsmith -> Desktop
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.agents.specialized.workflow_executor import WorkflowExecutor
from botsmith.memory import MemoryManager
from botsmith.llm.wrapper import OllamaLLM
import botsmith.agents


from botsmith.persistence.database import init_db
from botsmith.persistence.repository import WorkflowRepository

def test_workflow_executor():
    # Initialize DB for testing
    init_db()

    llm = OllamaLLM()
    mm = MemoryManager()
    factory = AgentFactory(llm, mm)
    repo = WorkflowRepository()

    executor = WorkflowExecutor(factory, repo)

    workflow_def = {
        "workflow_name": "bot_creation_workflow",
        "steps": [
            {"order": 1, "step": "analyze_requirements", "agent": "executor", "retry": 1, "on_failure": "abort"},
            {"order": 2, "step": "deployment", "agent": "executor", "retry": 1, "on_failure": "abort"},
        ],
    }

    result = executor.execute(
        workflow_def,
        initial_context={"dry_run": True}
    )

    print(result)


if __name__ == "__main__":
    test_workflow_executor()
