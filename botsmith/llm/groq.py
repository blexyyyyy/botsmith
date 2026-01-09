# botsmith/core/llm/groq.py

import os
from groq import Groq
from botsmith.core.interfaces.llm_interface import ILLMWrapper
from botsmith.core.exceptions.custom_exceptions import LLMUnavailableError


class GroqLLM(ILLMWrapper):
    def __init__(self, model: str = "llama3-8b-8192"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise LLMUnavailableError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = model

    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        chat = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return chat.choices[0].message.content
