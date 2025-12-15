import ast
from typing import Dict, Any
from botsmith.core.base.agent import BaseAgent


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
                    res = self._generate_single_file(fname, desc, request)
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

        return self._generate_single_file(filename, description, request)

    def _generate_single_file(self, filename: str, description: str, request: str) -> Dict[str, Any]:
        # Prompt for code
        prompt = f"""
Generate ONLY valid Python code for file: {filename}

Project request:
{request}

File purpose:
{description}

Rules:
1. Output only Python code (no markdown, no ``` blocks)
2. Include all needed imports
3. Add docstrings and comments
4. Must be runnable
5. If this is bot.py, include a main() and __main__ block
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
