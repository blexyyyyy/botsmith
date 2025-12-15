from typing import Dict, Any, List
from botsmith.core.base.agent import BaseAgent


class FilePlanAgent(BaseAgent):
    """
    Decides which Python files a project needs.
    This agent:
    - takes the user request + planner output
    - returns a clean file manifest
    - does NOT generate code
    - does NOT write to disk
    """

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:

        request = context.get("original_request", "")
        plan = context.get("plan", [])

        if not plan:
            raise ValueError("FilePlanAgent requires 'plan' in context")

        files = []

        # Always include main bot entry
        files.append({
            "filename": "bot.py",
            "description": "Main bot, command routing, execution entry point"
        })
        
        files.append({
            "filename": "README.md",
            "description": "Project documentation, setup instructions, and usage guide"
        })
        
        files.append({
            "filename": "requirements.txt",
            "description": "Python dependencies required"
        })

        # If API-related steps exist
        if any(step in plan for step in ["design_api", "implement_api"]):
            files.append({
                "filename": "api.py",
                "description": "API client or server logic for the bot"
            })

        # If agents are part of the plan
        if any(step in plan for step in ["define_agents", "configure_agents"]):
            files.append({
                "filename": "agents.py",
                "description": "Internal helper agents for bot logic"
            })

        # Minimal utility module for reusable helpers
        files.append({
            "filename": "utils.py",
            "description": "Helper functions, parsing, formatting"
        })

        # Remove duplicates & enforce order
        seen = set()
        manifest = []
        for f in files:
            if f["filename"] not in seen:
                manifest.append(f)
                seen.add(f["filename"])

        return {
            "status": "success",
            "files": manifest,
            "file_count": len(manifest)
        }
