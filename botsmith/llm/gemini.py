import os
import time
from typing import Optional
from google.api_core import exceptions

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from botsmith.core.interfaces.llm_interface import ILLMWrapper
from botsmith.core.exceptions.custom_exceptions import LLMUnavailableError


class GeminiLLM(ILLMWrapper):
    """
    Cloud LLM wrapper using Google Gemini API.
    Optimized for high-quality code generation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "models/gemini-1.5-flash",
    ):
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai"
            )

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not provided. "
                "Set GEMINI_API_KEY in .env or pass api_key parameter."
            )

        self.model_name = model
        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel(model)

    def is_available(self) -> bool:
        try:
            # Quick test
            return self.api_key is not None and GEMINI_AVAILABLE
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.is_available():
            raise LLMUnavailableError("Gemini is not available")

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        retries = 3
        delay = 2

        for attempt in range(retries):
            try:
                response = self._model.generate_content(full_prompt)
                return response.text
            except exceptions.ResourceExhausted:
                if attempt < retries - 1:
                    print(f"[Gemini] Rate limited. Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise LLMUnavailableError("Gemini quota exceeded after retries")
            except Exception as e:
                raise LLMUnavailableError(f"Gemini API error: {e}")

    def generate_code(self, prompt: str) -> str:
        """Specialized method for code generation with code-focused system prompt."""
        system_prompt = """You are an expert Python developer. Generate clean, working Python code.

Rules:
1. Output ONLY the Python code, no explanations before or after
2. Include necessary imports at the top
3. Add docstrings and comments for clarity
4. Make the code runnable as a standalone script
5. Include proper error handling
6. If it's a bot/agent, include a main() function and if __name__ == "__main__" block"""

        return self.generate(prompt, system_prompt)
