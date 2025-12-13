# botsmith/core/base/agent.py

from typing import Dict, Any, List
from abc import ABC
from ..interfaces.agent_interface import IAgent
from ..interfaces.llm_interface import ILLMWrapper
from ..interfaces.memory_interface import IMemoryManager
from ..exceptions.custom_exceptions import AgentExecutionError
from ..memory.models import AgentMemory


class BaseAgent(IAgent, ABC):
    """
    Base implementation of an agent.

    Handles:
    - LLM access
    - memory access
    - execution bookkeeping
    - error safety

    Subclasses are responsible for task-specific logic.
    """

    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        llm: ILLMWrapper,
        memory_manager: IMemoryManager,
        capabilities: List[str] | None = None,
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self._llm = llm
        self._memory_manager = memory_manager
        self._capabilities = capabilities or []

        # metrics
        self._execution_count = 0
        self._success_count = 0
        self._failure_count = 0

        # ensure memory exists
        if self._memory_manager.load_memory(agent_id) is None:
            self._memory_manager.save_memory(
                AgentMemory(agent_id=agent_id)
            )

    def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safe execution wrapper.
        """
        self._execution_count += 1

        try:
            result = self._execute(task, context)
            self._success_count += 1
            self._record_interaction(task, result, success=True)
            return result

        except Exception as e:
            self._failure_count += 1
            self._record_interaction(task, str(e), success=False)
            raise AgentExecutionError(
                f"Agent '{self.agent_id}' failed to execute task"
            ) from e

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actual task execution logic.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

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
