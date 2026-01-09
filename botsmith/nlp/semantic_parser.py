import json
from botsmith.core.interfaces.llm_interface import ILLMWrapper


class SemanticParser:
    """
    Uses an LLM to convert natural language into a structured draft intent.
    """

    SYSTEM_PROMPT = """
You are an intent extraction engine.

Given a user command, extract:
- intent (one of: build_bot, deploy, analyze, unknown)
- entities (as JSON)
- confidence (0.0 to 1.0)

Respond ONLY with valid JSON.
"""

    def __init__(self, llm: ILLMWrapper):
        self._llm = llm

    def parse(self, text: str) -> dict:
        response = self._llm.generate(
            prompt=text,
            system_prompt=self.SYSTEM_PROMPT,
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "intent": "unknown",
                "entities": {},
                "confidence": 0.0,
            }
