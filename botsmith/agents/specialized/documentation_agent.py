from typing import Dict, Any
from botsmith.agents.base_agent import BaseAgent

class DocumentationAgent(BaseAgent):
    """
    Generates documentation and text files (README, requirements).
    No code validation, just text generation.
    """

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        filename = context.get("filename")
        description = context.get("description")
        request = context.get("original_request", "")

        prompt = f"""
You are a technical writer for a Python project.
Generate the file content for: {filename}

Project Request:
{request}

File Purpose:
{description}

Rules:
1. Output ONLY the file content.
2. No markdown code blocks (unless the file itself is a markdown file, then use them appropriately for the content).
3. Be professional and detailed.
"""
        content = self._llm.generate(prompt)
        
        # Cleanup
        if filename.endswith(".txt") and content.startswith("```"):
             content = content.replace("```", "")
        
        # For md files, we generally keep the content as is, but remove outer "Here is the file" wrappers if any
        # Assuming model follows instruction "Output ONLY the file content"

        return {
            "filename": filename,
            "code": content, # Naming key 'code' to match executor expectation
            "validated": True
        }
