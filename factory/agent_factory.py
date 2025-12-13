# botsmith/factory/agent_factory.py

from typing import Dict, Any
from ..core.interfaces.llm_interface import ILLMWrapper
from ..core.interfaces.memory_interface import IMemoryManager
from ..core.interfaces.agent_interface import IAgent
from ..agents.registry import AgentRegistry
from .abstract_factory import AbstractAgentFactory


class AgentFactory(AbstractAgentFactory):
    def __init__(self, llm: ILLMWrapper, memory_manager: IMemoryManager):
        self.llm = llm
        self.memory_manager = memory_manager

    def create_agent(self, config: Dict[str, Any]) -> IAgent:
        agent_type = config.get("type")
        if not agent_type:
            raise ValueError("Agent configuration missing 'type' field")

        params = config.get("params", {})
        
        # Get class from registry
        agent_cls = AgentRegistry.get(agent_type)

        # Inject common dependencies if the agent class expects them
        # For now, we specifically handle the AutoGenAgent signature/known classes
        # But a generic approach would be better in the long run.
        
        # We assume params strictly matches constructor args for now, minus the memory_manager which we inject
        # For AutoGenAgent: Needs memory_manager. llm_config is in params.
        
        return agent_cls(
            llm=self.llm,
            memory_manager=self.memory_manager,
            **params
        )
