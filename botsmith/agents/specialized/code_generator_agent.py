import ast
from typing import Dict, Any
from botsmith.agents.base_agent import BaseAgent


class CodeGeneratorAgent(BaseAgent):
    """
    Generates Python code for a single file.
    - No filesystem access
    - Uses LLMRouter (inherits from BaseAgent)
    - Validates syntax
    """

    def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:

        filename = context.get("filename")
        description = context.get("description")
        files = context.get("files")
        request = context.get("original_request")

        # Case 1: Batch Mode (from FilePlanAgent)
        if files and isinstance(files, list):
            results = []
            for f in files:
                fname = f.get("filename")
                desc = f.get("description")
                if not fname: 
                    continue
                
                # Recursive call or inline? Inline is safer for now
                try:
                    # Pass the full list of files so the LLM knows what to import
                    project_structure = [x.get("filename") for x in files if x.get("filename")]
                    res = self._generate_single_file(fname, desc, request, project_structure)
                    results.append(res)
                except Exception as e:
                    results.append({"filename": fname, "error": str(e), "validated": False})
            
            return {
                "generated_files": results,
                "count": len(results),
                "status": "success"
            }

        # Case 2: Single Mode
        if not filename or not description:
            raise ValueError("filename/description OR files list required in context")

        project_structure = context.get("project_structure")
        return self._generate_single_file(filename, description, request, project_structure)

    def _generate_single_file(self, filename: str, description: str, request: str, project_files: list = None) -> Dict[str, Any]:
        # Context string for other files
        context_str = ""
        if project_files:
            context_str = "Project Structure (other files available):\n" + "\n".join([f"- {f}" for f in project_files])

        # Prompt for code
        prompt = f"""
You are a Senior Python Engineer. Generate production-grade code for: {filename}

Project Request:
{request}

File Purpose:
{description}

{context_str}

Rules:
1.  **Architecture**: Follow SOLID principles strictly.
    -   **SRP**: Keep classes focused.
    -   **DIP**: Depend on abstractions if possible.
2.  **Imports**: 
    -   You may import from other files listed in 'Project Structure' (e.g. `from config import settings`).
    -   Use absolute imports or relative imports correctly for a package named based on the project.
3.  **Quality**:
    -   Use Type Hinting (typing module).
    -   Include docstrings for classes and methods.
    -   Handle errors gracefully (try/except).
4.  **Entry Point**: 
    -   If this is `main.py`:
        -   CRITICAL: You MUST import and call functions/classes from other files in the project.
        -   The `main()` function should EXECUTE the bot's core logic (fetch data, process, save output, etc.).
        -   Do NOT just print "Bot is running" - actually implement the functionality described.
        -   Include `if __name__ == "__main__": main()`.
    -   If this is `requirements.txt`, list dependencies one per line (no code blocks).
5.  **Output**:
    -   Output ONLY the raw code/content.
    -   NO markdown blocking (```python).
    -   NO explanations.
"""

        code = self._llm.generate(prompt)
        
        # Clean markdown if present
        if code.startswith("```python"):
            code = code.replace("```python", "").replace("```", "")
        elif code.startswith("```"):
            code = code.replace("```", "")
            
        code = code.strip()

        # Validate syntax
        valid = self._validate(code)

        return {
            "filename": filename,
            "code": code,
            "validated": valid,
            "error": None if valid else "Syntax validation failed"
        }

    def _validate(self, code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
