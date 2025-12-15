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
        self._memory = self._memory_manager.load_memory(agent_id)
        if self._memory is None:
            self._memory = AgentMemory(
                agent_id=agent_id,
                interactions=[],
                metadata={},
            )

    def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safe execution wrapper with guaranteed persistence.
        """
        self._execution_count += 1
        result = None
        success = False

        try:
            result = self._execute(task, context)
            success = True
            self._success_count += 1
            return result

        except Exception as e:
            self._failure_count += 1
            result = str(e)
            raise AgentExecutionError(
                f"Agent '{self.agent_id}' failed to execute task: {str(e)}"
            ) from e

        finally:
            self._memory.interactions.append({
                "task": task,
                "result": result,
                "success": success,
            })
            self._memory_manager.save_memory(self._memory)

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actual task execution logic.
        Must be implemented by subclasses.
        """
        raise NotImplementedError



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
