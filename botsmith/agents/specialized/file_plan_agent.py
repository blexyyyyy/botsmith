from typing import Dict, Any, List
from botsmith.agents.base_agent import BaseAgent


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
        project_name = context.get("project_name", "bot")

        if not plan:
            # Fallback if no plan is provided, though usually it should be there.
            pass

        # 1. Construct Prompt
        prompt = f"""
You are an expert Python software architect.
Your goal is to design the file structure for a Python bot project based on the user's request.

User Request: "{request}"
Project Name: "{project_name}"

High-Level Plan:
{context.get('plan', 'No specific plan provided.')}

Requirements:
1.  **Entry Point**: You MUST include `main.py` as the entry point. 
    -   `main.py` MUST import and USE all service/utility files you define.
    -   `main.py` should contain a `main()` function that actually runs the bot's core logic by calling the services.
    -   Do NOT just print "Bot is running" - the bot must actually DO something.
2.  **SOLID Principles**:
    -   **Single Responsibility Principle (SRP)**: Split code into meaningful modules (e.g., `services/`, `models/`, `config.py`) rather than one big file.
    -   **Dependency Inversion**: If the bot relies on external APIs, consider creating service interfaces or separate classes.
3.  **Standard Files**: Include `requirements.txt`, `README.md`, and `.env` (if secrets are needed).
4.  **Output Format**: Return ONLY a valid JSON object with a "files" key, which is a list of objects containing "filename" and "description".
    -   IMPORTANT: All source files MUST be in `src/{project_name}/`.
    -   Example: `src/{project_name}/main.py`, `src/{project_name}/services/foo.py`.

Example JSON Structure:
{{
  "files": [
    {{ "filename": "src/{project_name}/main.py", "description": "Entry point. Imports WeatherService, calls fetch_weather(), and prints results." }},
    {{ "filename": "src/{project_name}/config.py", "description": "Configuration loader using environment variables." }},
    {{ "filename": "src/{project_name}/services/weather_service.py", "description": "Handles interactions with the Weather API." }}
  ]
}}

Give me the JSON now.
"""

        # 2. Call LLM
        response = self._llm.generate(prompt)

        # 3. Parse JSON
        import json
        import re

        files = []
        try:
            # Clean up potential markdown code blocks
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response.replace("```json", "").replace("```", "")
            elif clean_response.startswith("```"):
                clean_response = clean_response.replace("```", "")
            
            data = json.loads(clean_response)
            files = data.get("files", [])
        except json.JSONDecodeError:
            # Fallback if LLM fails (should rely on a retry or better parser, but for now simple fallback)
            # Log error ideally
            print(f"FilePlanAgent: Failed to parse JSON. Response: {response[:100]}...")
            files = [
                {"filename": "main.py", "description": "Main entry point (fallback due to parse error)."},
                {"filename": "requirements.txt", "description": "Dependencies."}
            ]

        # 4. Post-processing / Validation
        # Ensure main.py exists
        if not any(f["filename"].endswith("main.py") for f in files):
             p_name = context.get("project_name", "bot")
             files.insert(0, {"filename": f"src/{p_name}/main.py", "description": "Entry point."})

        return {
            "status": "success",
            "files": files,
            "file_count": len(files),
            "summary": f"Planned {len(files)} files: {', '.join([f['filename'] for f in files[:3]])}{'...' if len(files)>3 else ''}"
        }
