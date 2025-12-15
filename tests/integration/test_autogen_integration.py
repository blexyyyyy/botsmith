from botsmith.core.base.autogen_agent import AutoGenAgent
from botsmith.core.memory.manager import InMemoryMemoryManager
from unittest.mock import patch
from autogen import ConversableAgent # Assuming ConversableAgent is needed for patching

llm_config = {
    "model": "llama3",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}

mm = InMemoryMemoryManager()

agent = AutoGenAgent(
    agent_id="auto_1",
    name="test_agent",
    system_message="You are a helpful assistant.",
    llm_config=llm_config,
    memory_manager=mm,
    agent_type="conversable",
    capabilities=["chat"],
)

# Mock the ConversableAgent (or AutoGenAgent's internal agent)
with patch("autogen.ConversableAgent.generate_reply", return_value="Hello! This is a mocked response."):
    result = agent.execute("Say hello in one sentence.", {})

print("Result:", result)
assert result["response"] == "Hello! This is a mocked response."
