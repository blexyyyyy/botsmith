# botsmith/core/base/autogen_agent.py

from typing import Any, Dict, List

try:
    from autogen import AssistantAgent, ConversableAgent, UserProxyAgent
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    AssistantAgent = None
    ConversableAgent = None
    UserProxyAgent = None

from ..exceptions.custom_exceptions import AgentExecutionError
from ..interfaces.agent_interface import IAgent
from ..interfaces.memory_interface import IMemoryManager
from ..memory.models import AgentMemory


class AutoGenAgent(IAgent):
    """
    Adapter that wraps AutoGen agents and exposes them as IAgent.
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        system_message: str,
        llm_config: Dict[str, Any],
        memory_manager: IMemoryManager,
        agent_type: str = "conversable",
        capabilities: List[str] | None = None,
    ):
        self.agent_id = agent_id
        self.name = name
        self._capabilities = capabilities or []
        self._memory_manager = memory_manager

        self._execution_count = 0
        self._success_count = 0
        self._failure_count = 0

        self._autogen_agent = self._create_autogen_agent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            agent_type=agent_type,
        )

        if self._memory_manager.load_memory(agent_id) is None:
            self._memory_manager.save_memory(
                AgentMemory(agent_id=agent_id)
            )

    def _create_autogen_agent(
        self,
        name: str,
        system_message: str,
        llm_config: Dict[str, Any],
        agent_type: str,
    ):
        if agent_type == "assistant":
            return AssistantAgent(
                name=name,
                system_message=system_message,
                llm_config=llm_config,
            )
        elif agent_type == "user_proxy":
            return UserProxyAgent(
                name=name,
                system_message=system_message,
                llm_config=llm_config,
            )
        else:
            return ConversableAgent(
                name=name,
                system_message=system_message,
                llm_config=llm_config,
            )

    def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        self._execution_count += 1

        try:
            response = self._autogen_agent.generate_reply(
                messages=[{"role": "user", "content": task}]
            )

            self._success_count += 1
            self._record_interaction(task, response, success=True)

            return {
                "agent": self.agent_id,
                "response": response,
            }

        except Exception as e:
            self._failure_count += 1
            self._record_interaction(task, str(e), success=False)

            raise AgentExecutionError(
                f"AutoGenAgent '{self.agent_id}' failed"
            ) from e

    def _record_interaction(self, task: str, output: Any, success: bool):
        memory = self._memory_manager.load_memory(self.agent_id)
        if memory is None:
            return

        memory.interactions.append(
            {
                "task": task,
                "output": output,
                "success": success,
            }
        )
        self._memory_manager.save_memory(memory)

    def get_capabilities(self) -> List[str]:
        return self._capabilities

    def get_performance_metrics(self) -> Dict[str, float]:
        success_rate = (
            self._success_count / self._execution_count
            if self._execution_count > 0
            else 0.0
        )

        return {
            "executions": self._execution_count,
            "successes": self._success_count,
            "failures": self._failure_count,
            "success_rate": success_rate,
        }
