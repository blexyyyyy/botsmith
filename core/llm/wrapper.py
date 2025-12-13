# botsmith/core/llm/wrapper.py

import requests
from typing import Optional
from ..interfaces.llm_interface import ILLMWrapper
from ..exceptions.custom_exceptions import LLMUnavailableError


class OllamaLLM(ILLMWrapper):
    """
    Local LLM wrapper using Ollama.
    """

    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def is_available(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.is_available():
            raise LLMUnavailableError("Ollama is not running or unreachable")

        payload = {
            "model": self.model,
            "prompt": prompt if not system_prompt else f"{system_prompt}\n\n{prompt}",
            "stream": False,
        }

        resp = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=60,
        )

        resp.raise_for_status()
        return resp.json().get("response", "")
