import os
import re
import ast
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

from botsmith.core.base.agent import BaseAgent
from botsmith.core.llm.gemini import GeminiLLM

# Load environment variables
load_dotenv()


class CodeGeneratorAgent(BaseAgent):
    """
    Generates actual Python code using Gemini and saves to files.
    Generates file-by-file with validation after each file.
    """

    GENERATED_DIR = Path(__file__).resolve().parent.parent.parent / "generated"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use Gemini for high-quality code generation
        try:
            self._code_llm = GeminiLLM()
        except (ImportError, ValueError) as e:
            # Fallback to the injected LLM if Gemini not available
            print(f"[CodeGenerator] Gemini not available: {e}, using fallback LLM")
            self._code_llm = self._llm

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        project_name = context.get("project_name", "untitled_project")
        original_request = context.get("original_request", task)
        plan = context.get("plan", [])

        # Step 1: Get file structure from LLM
        file_structure = self._plan_file_structure(original_request, plan)
        
        # Step 2: Generate each file with validation
        generated_files = []
        errors = []
        
        for file_info in file_structure:
            filename = file_info["filename"]
            description = file_info["description"]
            
            try:
                code = self._generate_file(original_request, filename, description)
                
                # Validate syntax
                if self._validate_python_syntax(code):
                    file_path = self._save_file(project_name, filename, code)
                    generated_files.append({
                        "filename": filename,
                        "path": str(file_path),
                        "size": len(code),
                        "validated": True,
                    })
                else:
                    errors.append({"filename": filename, "error": "Syntax validation failed"})
                    
            except Exception as e:
                errors.append({"filename": filename, "error": str(e)})

        return {
            "status": "success" if generated_files else "failed",
            "project_name": project_name,
            "files_generated": len(generated_files),
            "files": generated_files,
            "errors": errors,
        }

    def _plan_file_structure(self, request: str, plan: List[str]) -> List[Dict]:
        """Ask LLM to plan which files to generate."""
        prompt = f"""For this request: "{request}"

List the Python files needed. For each file, provide:
- filename (e.g., bot.py, utils.py)
- description (what this file should contain)

Respond in this exact format, one file per line:
filename: description

Keep it minimal - usually 1-3 files max. Always include a main bot.py file."""

        response = self._code_llm.generate(prompt)
        
        files = []
        for line in response.strip().split("\n"):
            if ":" in line:
                parts = line.split(":", 1)
                filename = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ""
                if filename.endswith(".py"):
                    files.append({"filename": filename, "description": description})
        
        # Ensure at least bot.py exists
        if not any(f["filename"] == "bot.py" for f in files):
            files.insert(0, {"filename": "bot.py", "description": "Main bot implementation"})
        
        return files[:5]  # Limit to 5 files

    def _generate_file(self, request: str, filename: str, description: str) -> str:
        """Generate code for a single file using Gemini."""
        prompt = f"""Create the file `{filename}` for this project: "{request}"

File purpose: {description}

Requirements:
1. Output ONLY valid Python code, no markdown, no explanations
2. Include all necessary imports
3. Add docstrings and comments
4. Make it runnable
5. Include error handling
6. If this is bot.py, include a main() function and if __name__ == "__main__" block"""

        code = self._code_llm.generate(prompt)
        return self._extract_code(code)

    def _extract_code(self, response: str) -> str:
        """Extract Python code from LLM response, handling markdown blocks."""
        # Check for ```python blocks
        code_match = re.search(r"```python\s*(.*?)\s*```", response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # Check for generic ``` blocks
        code_match = re.search(r"```\s*(.*?)\s*```", response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # Assume entire response is code
        return response.strip()

    def _validate_python_syntax(self, code: str) -> bool:
        """Validate Python syntax using ast.parse."""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            print(f"[CodeGenerator] Syntax error: {e}")
            return False

    def _save_file(self, project_name: str, filename: str, code: str) -> Path:
        """Save generated code to a file."""
        # Sanitize project name
        safe_name = re.sub(r"[^\w\-]", "_", project_name.lower().replace(" ", "_"))
        
        # Create project directory
        project_dir = self.GENERATED_DIR / safe_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = project_dir / filename
        file_path.write_text(code, encoding="utf-8")
        
        # Create __init__.py if not exists
        init_path = project_dir / "__init__.py"
        if not init_path.exists():
            init_path.write_text(f'"""Generated project: {project_name}"""\n', encoding="utf-8")
        
        print(f"[CodeGenerator] Saved: {file_path}")
        return file_path
