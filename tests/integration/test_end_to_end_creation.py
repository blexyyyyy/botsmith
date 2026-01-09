import sys
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from botsmith.factory.agent_factory import AgentFactory
from botsmith.persistence.database import init_db
from botsmith.persistence.repository import WorkflowRepository, AgentRepository
from botsmith.persistence.models import AgentRecord
from botsmith.memory.sqlite_manager import SQLiteMemoryManager
from botsmith.llm.wrapper import OllamaLLM
from botsmith.tools.filesystem import FileSystemTool
import botsmith.agents


def test_end_to_end_creation():
    print("=== Starting End-to-End Bot Creation Test (Real Ollama) ===")
    
    # 1. Setup
    init_db()
    llm = OllamaLLM()
    mm = SQLiteMemoryManager()
    factory = AgentFactory(llm, mm)
    workflow_repo = WorkflowRepository()
    agent_repo = AgentRepository()
    
    fs = FileSystemTool(base_dir="generated_bots")

    # [omitted agent creation helper...]
    def create_and_save_agent(agent_type: str, agent_id: str, capabilities: list = None):
        config = {"agent_id": agent_id, "agent_type": "logic", "capabilities": capabilities or []}
        agent = factory.create_agent({"type": agent_type, "params": config})
        
        # Save to DB
        agent_repo.save_agent(AgentRecord(
            agent_id=agent_id,
            agent_type=agent_type,
            capabilities=capabilities or [],
            config=config,
        ))
        print(f"    [DB] Saved agent: {agent_id}")
        return agent
    
    print("\n[0] Creating and Persisting Agents...")
    router = create_and_save_agent("router", "router_main", ["routing"])
    planner = create_and_save_agent("planner", "planner_main", ["planning"])
    validator = create_and_save_agent("validator", "validator_main", ["validation"])
    compiler = create_and_save_agent("workflow_compiler", "compiler_main", ["compilation"])
    cost_estimator = create_and_save_agent("cost_estimator", "cost_main", ["cost_estimation"])
    security = create_and_save_agent("security", "sec_main", ["security_scan"])
    optimizer = create_and_save_agent("optimizer", "opt_main", ["optimization"])
    project_scaffold = create_and_save_agent("scaffolder", "scaffold_main", ["scaffolding"])
    
    # Workflow Executor (manual instantiation for repo injection)
    from botsmith.agents.specialized.workflow_executor import WorkflowExecutor
    workflow_executor = WorkflowExecutor(factory, workflow_repo)


    user_request = "Build a python weather bot"
    project_name = "weather_bot"
    context = {
        "original_request": user_request,
        "project_name": project_name,
    }
    
    # 2. Routing
    print(f"\n[1] Routing Task: '{user_request}'")
    route_result = router.execute(user_request, context)
    print(f"    -> Route: {route_result.get('route')}")
    assert route_result["route"] == "bot_creation_workflow"
    context.update(route_result)

    # 3. Planning
    print(f"\n[2] Generating Plan...")
    plan_result = planner.execute(user_request, context)
    print(f"    -> Plan: {plan_result.get('plan')}")
    assert "plan" in plan_result
    context.update(plan_result)

    # 4. Validation
    print(f"\n[3] Validating Plan...")
    valid_result = validator.execute("validate plan", context)
    print(f"    -> Valid: {valid_result.get('valid')}")
    if not valid_result.get('valid'):
        print(f"    -> Errors: {valid_result.get('errors')}")
        print(f"    -> Plan being validated: {context.get('plan')}")
    assert valid_result["valid"] is True
    context.update({"validation": valid_result})

    # 5. Compilation
    print(f"\n[4] Compiling Workflow...")
    compile_result = compiler.execute("compile workflow", context)
    workflow_def = compile_result
    print(f"    -> Steps: {len(workflow_def.get('steps', []))}")
    assert len(workflow_def["steps"]) > 0
    
    # 6. Pre-Execution Checks (Cost, Security, Opt)
    print(f"\n[5] Running Pre-flight Checks (Cost, Security, Optimizer)...")
    
    cost_res = cost_estimator.execute("estimate", {"steps": workflow_def["steps"]})
    print(f"    -> Cost: ${cost_res['estimated_cost']}")
    
    sec_res = security.execute("scan", {"steps": workflow_def["steps"]})
    print(f"    -> Secure: {sec_res['secure']}")
    assert sec_res["secure"] is True
    
    opt_res = optimizer.execute("optimize", {"steps": workflow_def["steps"]})
    print(f"    -> Optimized Steps: {opt_res['optimized_count']}")
    
    # Update workflow with optimized steps
    workflow_def["steps"] = opt_res["optimized_steps"]

    # 7. Execution (with code generation!)
    print(f"\n[6] Executing Workflow (Generating Code)...")
    # Pass full context for code generator to use
    exec_context = {
        **context,
        "dry_run": False,  # Actually generate code!
        "filesystem": fs,
    }
    exec_result = workflow_executor.execute(workflow_def, initial_context=exec_context)
    
    print(f"    -> Status: {exec_result['status']}")
    if exec_result["status"] != "success":
        print(f"    -> Failed Step: {exec_result.get('failed_step')}")
        print(f"    -> Error: {exec_result.get('error')}")
        print(f"    -> Log: {json.dumps(exec_result.get('log'), indent=2, default=str)}")
        
    print(f"    -> Log: {len(exec_result.get('log', []))} steps executed")
    
    assert exec_result["status"] == "success"

    # Verifying scaffolding
    project_name = context["project_name"]
    assert fs.exists(f"{project_name}/src/{project_name}/main.py")
    assert fs.exists(f"{project_name}/requirements.txt")
    assert fs.exists(f"{project_name}/README.md")
    
    # Optional strict check
    # assert exec_result["final_context"].get("scaffolded") is True
    
    print("\n=== End-to-End Test PASSED ===")

if __name__ == "__main__":
    test_end_to_end_creation()
