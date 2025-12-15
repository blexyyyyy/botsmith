import sys
import os
from unittest.mock import MagicMock, patch

# Create relative path to the root context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from botsmith.core.base.autogen_agent import AutoGenAgent
from botsmith.core.memory.manager import InMemoryMemoryManager
from botsmith.workflows.workflow_factory import WorkflowFactory
from botsmith.workflows.workflow_executor import WorkflowExecutor
from botsmith.factory.agent_factory import AgentFactory
from botsmith.core.llm.wrapper import OllamaLLM

def test_workflow_execution():
    # Setup dependencies
    llm = OllamaLLM()
    mm = InMemoryMemoryManager()
    agent_factory = AgentFactory(llm, mm)
    
    # Create agents
    # We need a planner agent for the factory
    planner = AutoGenAgent(
        agent_id="planner", 
        name="Planner", 
        system_message="Plan.", 
        llm_config={"model": "llama3", "api_key": "ollama", "base_url": "http://localhost:11434/v1"}, 
        memory_manager=mm
    )
    
    # 1. Factory phase
    workflow_factory = WorkflowFactory(planner)
    
    # Mock planner execution to return a simple plan
    with patch.object(AutoGenAgent, 'execute') as mock_planner_exec:
        mock_planner_exec.return_value = {
            "plan": ["define_agents"],
            "project_name": "test_bot"
        }
        context = {}
        workflow_def = workflow_factory.create_workflow("Build a bot", context)
        
        assert workflow_def["workflow_name"] == "bot_creation_workflow"
        assert len(workflow_def["steps"]) > 0
        
        # 2. Execution phase
        executor = WorkflowExecutor(agent_factory)
        
        # Mock executor steps to avoid real agent creation/execution loop complexity in this unit test
        # But we do want to verify the executor logic itself.
        # We can mock AgentFactory.create_agent to return a mock agent
        
        mock_agent = MagicMock()
        mock_agent.execute.return_value = {"status": "done"}
        
        with patch.object(AgentFactory, 'create_agent', return_value=mock_agent):
            result = executor.execute(workflow_def, context)
            
            assert result["status"] == "success"
            assert len(result["log"]) > 0

if __name__ == "__main__":
    test_workflow_execution()
