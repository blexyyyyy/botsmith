from botsmith.core.base.agent import BaseAgent
from botsmith.core.memory.manager import InMemoryMemoryManager
from botsmith.core.llm.wrapper import OllamaLLM


class EchoAgent(BaseAgent):
    def _execute(self, task, context):
        return {"echo": task}


mm = InMemoryMemoryManager()
llm = OllamaLLM()

agent = EchoAgent(
    agent_id="echo_1",
    agent_type="test",
    llm=llm,
    memory_manager=mm,
    capabilities=["echo"],
)

print(agent.execute("hello", {}))
print(agent.get_performance_metrics())
