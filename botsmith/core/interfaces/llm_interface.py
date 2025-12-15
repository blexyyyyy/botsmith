# botsmith/core/interfaces/llm_interface.py

from abc import ABC, abstractmethod


class ILLMWrapper(ABC):
    """
    Abstraction over any LLM provider (Groq, Gemini, OpenAI, local).
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: User or agent prompt
            system_prompt: Optional system-level instructions

        Returns:
            Generated text response
        """
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the LLM backend is reachable and usable.
        """
        raise NotImplementedError
