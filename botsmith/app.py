import os
import json
from typing import Dict, Any, List
from pathlib import Path
from botsmith.config import settings

from botsmith.core.utils.config_loader import ConfigLoader
from botsmith.core.memory.manager import InMemoryMemoryManager
from botsmith.core.memory.sqlite_manager import SQLiteMemoryManager

from botsmith.core.llm.llm_router import LLMRouter
from botsmith.core.llm.wrapper import OllamaLLM
from botsmith.core.llm.gemini import GeminiLLM
from botsmith.core.llm.groq import GroqLLM

from botsmith.factory.agent_factory import AgentFactory
from botsmith.workflows.workflow_executor import WorkflowExecutor
from botsmith.workflows.workflow_factory import WorkflowFactory

from botsmith.agents.registry import AgentRegistry


class BotSmithApp:
    """
    Main orchestrator for BotSmith.
    Handles:
    - LLM setup
    - Memory setup
    - AgentFactory
    - WorkflowFactory
    - WorkflowExecutor
    """

    def __init__(self, config_path: str = None):
        # -------------------------
        # Load configuration
        # -------------------------
        if config_path is None:
            # Default to package-internal config/settings.py
            base_dir = Path(__file__).parent
            config_path = str(base_dir / "config" / "settings.py")

        self.config = ConfigLoader.load(config_path)

        # -------------------------
        # Memory system
        # -------------------------
        if getattr(self.config, "use_sqlite_memory", False):
            self.memory_manager = SQLiteMemoryManager(
                db_path=self.config.sqlite_memory_path
            )
        else:
            self.memory_manager = InMemoryMemoryManager()

        # -------------------------
        # LLM Setup (Router)
        # -------------------------
        self.local_llm = OllamaLLM(model=self.config.local_model)
        self.code_llm_instance = OllamaLLM(model=getattr(self.config, "code_model", "qwen2.5-coder"))

        # Cloud backups (optional)
        try:
            self.gemini_llm = GeminiLLM()
        except Exception:
            self.gemini_llm = None

        try:
            self.groq_llm = GroqLLM()
        except Exception:
            self.groq_llm = None

        self.llm = LLMRouter(
            local_llm=self.local_llm,
            gemini_llm=self.gemini_llm,
            groq_llm=self.groq_llm,
        )

        # -------------------------
        # Factories
        # -------------------------
        # Pass dedicated code LLM to factory
        self.agent_factory = AgentFactory(
            local_llm=self.llm, 
            memory_manager=self.memory_manager,
            code_llm=self.code_llm_instance
        )

        # Planner instance for WorkflowFactory
        planner_cls = AgentRegistry.get("planner")
        self.planner = planner_cls(
            agent_id="planner", 
            agent_type="planner", 
            llm=self.llm, 
            memory_manager=self.memory_manager
        )

        # Plugin Manager
        from botsmith.core.plugin import PluginManager
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

        self.workflow_factory = WorkflowFactory(self.planner, plugin_manager=self.plugin_manager)

        # Executor
        self.executor = WorkflowExecutor(self.agent_factory)

    # ----------------------------------------------------------------------
    # MAIN ENTRY POINT
    # ----------------------------------------------------------------------
    def create_bot(self, user_request: str, project_name: str, on_event=None) -> Dict[str, Any]:
        """
        Full end-to-end pipeline:
        1. Build workflow
        2. Execute workflow
        3. Return results + generated files
        """

        from botsmith.core.utils.filesystem import LocalFileSystem
        
        # Determine output root. For dev, relative to CWD/generated
        # or use a configured path.
        fs_root = Path("generated")
        fs = LocalFileSystem(str(fs_root))

        # Sanitize project name: strip trailing spaces, replace spaces with underscores, lowercase
        sanitized_name = project_name.strip().lower().replace(" ", "_")
        
        context = {
            "original_request": user_request,
            "project_name": sanitized_name,
            "dry_run": False,
            "filesystem": fs,
        }

        workflow_def = self.workflow_factory.create_workflow(
            user_request=user_request,
            context=context
        )
        
        # Emit initial event if callback provided
        if on_event:
             on_event("workflow_start", {"name": workflow_def.get("workflow_name"), "steps": len(workflow_def.get("steps", []))})

        result = self.executor.execute(workflow_def, context, on_event)

        return {
            "workflow": workflow_def,
            "result": result,
        }
