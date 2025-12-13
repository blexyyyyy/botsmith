from botsmith.core.base.autogen_agent import AutoGenAgent
from botsmith.core.memory.manager import InMemoryMemoryManager

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

result = agent.execute("Say hello in one sentence.", {})
print(result)
print(agent.get_performance_metrics())
