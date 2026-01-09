# botsmith/core/base/agent.py

from typing import Dict, Any, List
from abc import ABC
from botsmith.core.interfaces.agent_interface import IAgent
from botsmith.core.interfaces.llm_interface import ILLMWrapper
from botsmith.core.interfaces.memory_interface import IMemoryManager
from botsmith.core.exceptions.custom_exceptions import AgentExecutionError
from botsmith.core.memory import AgentMemory, MemoryUpdateProposal, MemoryScope, ExecutionContext


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
        Safe execution wrapper with guaranteed persistence and scoped memory.
        """
        self._execution_count += 1
        
        # STEP 3: Execution Context (Ephemeral)
        exec_context = ExecutionContext(agent_id=self.agent_id)
        
        result = None
        success = False

        try:
            # We pass the execution context into _execute if the subclass supports it,
            # but for now we keep the interface IAgent for compatibility.
            # Subclasses can access self._current_exec_context if needed.
            self._current_exec_context = exec_context
            
            result = self._execute(task, context)
            success = True
            self._success_count += 1
            return result

        except Exception as e:
            self._failure_count += 1
            result = str(e)
            exec_context.add_error(result)
            raise AgentExecutionError(
                f"Agent '{self.agent_id}' failed to execute task: {str(e)}"
            ) from e

        finally:
            # STEP 7: Propose interaction log to Session Memory
            proposal = MemoryUpdateProposal(
                key=f"interaction_{self._execution_count}",
                value={
                    "task": task,
                    "result": result,
                    "success": success,
                    "exec_context": exec_context.to_dict()
                },
                confidence=1.0, # High confidence in own record
                justification="Agent execution log",
                suggested_scope=MemoryScope.PROJECT,
                source=f"agent:{self.agent_id}"
            )
            self._memory_manager.propose(proposal)
            self._current_exec_context = None

    def propose_memory_update(self, key: str, value: Any, confidence: float, justification: str, scope: MemoryScope = None):
        """
        STEP 7: Agents only PROPOSE updates.
        """
        proposal = MemoryUpdateProposal(
            key=key,
            value=value,
            confidence=confidence,
            justification=justification,
            suggested_scope=scope,
            source=f"agent:{self.agent_id}"
        )
        return self._memory_manager.propose(proposal)

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
