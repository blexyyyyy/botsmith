from botsmith.agents.registry import AgentRegistry
from botsmith.core.base.autogen_agent import AutoGenAgent
from botsmith.agents.specialized.planner_agent import PlannerAgent
from botsmith.agents.specialized.validator_agent import ValidatorAgent
from botsmith.agents.specialized.router_agent import RouterAgent
from botsmith.agents.specialized.executor_agent import ExecutorAgent
from botsmith.agents.specialized.workflow_compiler_agent import WorkflowCompilerAgent
from botsmith.agents.specialized.workflow_executor import WorkflowExecutor
from botsmith.agents.specialized.cost_estimator_agent import CostEstimatorAgent
from botsmith.agents.specialized.security_agent import SecurityAgent
from botsmith.agents.specialized.workflow_optimizer_agent import WorkflowOptimizerAgent
from botsmith.agents.specialized.nlp_interpreter_agent import NLPInterpreterAgent
from botsmith.agents.specialized.code_generator_agent import CodeGeneratorAgent









AgentRegistry.register("autogen", AutoGenAgent)
AgentRegistry.register("planner", PlannerAgent)
AgentRegistry.register("validator", ValidatorAgent)
AgentRegistry.register("router", RouterAgent)
AgentRegistry.register("executor", ExecutorAgent) 
AgentRegistry.register("workflow_compiler", WorkflowCompilerAgent)
AgentRegistry.register("workflow_executor", WorkflowExecutor)
AgentRegistry.register("cost_estimator", CostEstimatorAgent)
AgentRegistry.register("security", SecurityAgent)
AgentRegistry.register("workflow_optimizer", WorkflowOptimizerAgent)
AgentRegistry.register("nlp_interpreter", NLPInterpreterAgent)
AgentRegistry.register("code_generator", CodeGeneratorAgent)