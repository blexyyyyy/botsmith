import sys
import os

# Create relative path to the root context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from botsmith.core.base.autogen_agent import AutoGenAgent
from botsmith.core.memory.manager import InMemoryMemoryManager
from botsmith.workflows.bot_creation_workflow import BotCreationWorkflow
from botsmith.autogen.managers.conversation_orchestrator import ConversationOrchestrator

llm_cfg = {
    "model": "llama3",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama"
}

mm = InMemoryMemoryManager()

analyzer = AutoGenAgent(
    agent_id="analyzer",
    name="Analyzer",
    system_message="Analyze requirements.",
    llm_config=llm_cfg,
    memory_manager=mm,
)

coder = AutoGenAgent(
    agent_id="coder",
    name="Coder",
    system_message="Write code.",
    llm_config=llm_cfg,
    memory_manager=mm,
)

validator = AutoGenAgent(
    agent_id="validator",
    name="Validator",
    system_message="Validate code.",
    llm_config=llm_cfg,
    memory_manager=mm,
)

workflow = BotCreationWorkflow(analyzer, coder, validator)
orchestrator = ConversationOrchestrator(workflow)

result = orchestrator.run(
    {"prompt": "Build a simple hello-world API"}
)

print(result.keys())
print("Analysis output keys:", result.get("analysis", {}).keys())
print("Workflow execution complete.")
