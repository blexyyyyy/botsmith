# botsmith/agents/registry.py

from typing import Dict, Type
from botsmith.core.interfaces.agent_interface import IAgent

# Import specialized agents
from botsmith.agents.specialized.planner_agent import PlannerAgent
from botsmith.agents.specialized.executor_agent import ExecutorAgent
from botsmith.agents.specialized.code_generator_agent import CodeGeneratorAgent
from botsmith.agents.specialized.project_scaffold_agent import ProjectScaffoldAgent
from botsmith.agents.specialized.nlp_interpreter_agent import NLPInterpreterAgent
from botsmith.agents.specialized.file_plan_agent import FilePlanAgent
from botsmith.agents.specialized.workflow_optimizer_agent import WorkflowOptimizerAgent
from botsmith.agents.specialized.documentation_agent import DocumentationAgent
from botsmith.agents.specialized.validator_agent import ValidatorAgent
from botsmith.agents.specialized.security_agent import SecurityAgent
from botsmith.agents.specialized.cost_estimator_agent import CostEstimatorAgent
from botsmith.agents.specialized.router_agent import RouterAgent
from botsmith.agents.specialized.workflow_compiler_agent import WorkflowCompilerAgent
from botsmith.core.base.autogen_agent import AutoGenAgent


class AgentRegistry:
    """
    Registry for all available agent types.
    """

    _REGISTRY: Dict[str, Type[IAgent]] = {
        "planner": PlannerAgent,
        "executor": ExecutorAgent,
        "coder": CodeGeneratorAgent,
        "scaffolder": ProjectScaffoldAgent,
        "nlp": NLPInterpreterAgent,
        "file_planner": FilePlanAgent,
        "optimizer": WorkflowOptimizerAgent,
        "doc_writer": DocumentationAgent,
        "validator": ValidatorAgent,
        "security": SecurityAgent,
        "cost_estimator": CostEstimatorAgent,
        "router": RouterAgent,
        "workflow_compiler": WorkflowCompilerAgent,
        "autogen": AutoGenAgent,
    }

    @classmethod
    def get(cls, agent_type: str) -> Type[IAgent]:
        if agent_type not in cls._REGISTRY:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls._REGISTRY[agent_type]

    @classmethod
    def list_available(cls):
        return list(cls._REGISTRY.keys())
