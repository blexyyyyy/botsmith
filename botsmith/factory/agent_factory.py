# botsmith/factory/agent_factory.py

from typing import Dict, Any

from botsmith.core.interfaces.agent_interface import IAgent
from botsmith.core.interfaces.llm_interface import ILLMWrapper
from botsmith.core.interfaces.memory_interface import IMemoryManager

from botsmith.agents.registry import AgentRegistry
from botsmith.factory.abstract_factory import AbstractAgentFactory


class AgentFactory(AbstractAgentFactory):
    """
    Centralized agent creation with dependency injection.

    Responsibilities:
    - Instantiate agents from registry
    - Inject memory manager
    - Select appropriate LLM per agent type
    - Keep agents dumb and factories smart
    """

    def __init__(
        self,
        local_llm: ILLMWrapper,
        memory_manager: IMemoryManager,
        code_llm: ILLMWrapper | None = None,
    ):
        # Local-first LLM (Devstral via Ollama)
        self.local_llm = local_llm

        # Code-capable LLM (can be same as local, or router)
        self.code_llm = code_llm or local_llm

        self.memory_manager = memory_manager

    def create_agent(self, config: Dict[str, Any]) -> IAgent:
        agent_type = config.get("type")
        if not agent_type:
            raise ValueError("Agent configuration missing 'type' field")

        params = config.get("params", {})

        # Resolve agent class
        agent_cls = AgentRegistry.get(agent_type)
        if not agent_cls:
            raise ValueError(f"Agent type '{agent_type}' not registered")

        # Select correct LLM for this agent
        llm = self._select_llm(agent_type)

        # Default agent_type to the registry key if not specified in params
        if "agent_type" not in params:
            params["agent_type"] = agent_type

        # Instantiate agent with injected dependencies
        return agent_cls(
            llm=llm,
            memory_manager=self.memory_manager,
            **params,
        )

    def _select_llm(self, agent_type: str) -> ILLMWrapper:
        """
        Decide which LLM an agent receives.

        Rules:
        - Code-heavy agents → code_llm
        - Logic / governance agents → local_llm
        """

        code_agents = {
            "coder",
            "code_generator",
            "project_scaffold",
            "nlp",
            "doc_writer",
        }

        if agent_type in code_agents:
            return self.code_llm

        return self.local_llm
