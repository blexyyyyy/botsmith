import sys
import os
from botsmith.config import settings
from botsmith.core.llm.wrapper import OllamaLLM
from botsmith.agents.specialized.code_generator_agent import CodeGeneratorAgent

from botsmith.core.memory.sqlite_manager import SQLiteMemoryManager

def test_coder():
    print("--- Starting Coder Debug ---")
    
    # Setup real DB
    db_path = "debug_botsmith.db"
    mem_manager = SQLiteMemoryManager(db_path=db_path)
    print(f"Settings Local Model: {settings.local_model}")
    print(f"Settings Code Model: {settings.code_model}")
    
    try:
        # Initialize LLM
        print("Initializing LLM...")
        llm = OllamaLLM(model=settings.code_model)
        
        # Check availability
        print(f"Checking availability at {llm.base_url}...")
        is_avail = llm.is_available()
        print(f"LLM Available: {is_avail}")
        
        if not is_avail:
            print("ERROR: LLM not available. Check Ollama.")
            return

        # Initialize Agent
        print("Initializing Agent...")
        agent = CodeGeneratorAgent(
            agent_id="test_coder",
            agent_type="coder",
            llm=llm,
            memory_manager=mem_manager
        )
        
        # Execute Task
        print("Executing Task...")
        context = {
            "filename": "debug_test.py",
            "description": "A simple python script that prints hello world.",
            "original_request": "Create a hello world script"
        }
        
        result = agent.execute("generate_code", context)
        print("Execution Result:")
        print(result)
        
    except Exception as e:
        print("EXCEPTION OCCURRED:")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_coder()
