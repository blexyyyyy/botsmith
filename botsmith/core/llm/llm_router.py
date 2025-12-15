# botsmith/core/llm/llm_router.py

from botsmith.core.interfaces.llm_interface import ILLMWrapper


class LLMRouter(ILLMWrapper):
    """
    Local-first LLM router for BotSmith.

    - Qwen2.5-Coder (local) is ALWAYS primary for code
    - Gemini is FIRST cloud fallback
    - Groq is SECOND cloud fallback
    - Planning/reasoning ALWAYS uses local Qwen
    - Nothing in the system is allowed to crash due to cloud issues
    """

    def __init__(
        self,
        local_llm: ILLMWrapper,
        gemini_llm: ILLMWrapper | None = None,
        groq_llm: ILLMWrapper | None = None,
    ):
        self.local_llm = local_llm
        self.gemini_llm = gemini_llm
        self.groq_llm = groq_llm

    def is_available(self) -> bool:
        return self.local_llm.is_available()

    def generate(self, prompt: str, system_prompt: str = "") -> str:

        if self._is_code_task(prompt):
            # 1️⃣ Local Qwen first (free, strong, reliable)
            try:
                return self.local_llm.generate(prompt, system_prompt)
            except:
                pass

            # 2️⃣ Gemini (best quality)
            if self.gemini_llm and self.gemini_llm.is_available():
                try:
                    if hasattr(self.gemini_llm, "generate_code"):
                        return self.gemini_llm.generate_code(prompt)
                    return self.gemini_llm.generate(prompt)
                except:
                    pass

            # 3️⃣ Groq
            if self.groq_llm and self.groq_llm.is_available():
                try:
                    return self.groq_llm.generate(prompt)
                except:
                    pass

            # 4️⃣ Final fallback (never fail)
            return self.local_llm.generate(prompt)

        # Non-code → always use Qwen locally
        return self.local_llm.generate(prompt, system_prompt)

    def _is_code_task(self, prompt: str) -> bool:
        p = prompt.lower()
        return any(
            key in p
            for key in (
                "write code",
                "generate code",
                "implement",
                "fix this",
                "refactor",
                "build a bot",
                "build an api",
                "python file",
                "module",
                "class ",
                "def ",
                "script",
            )
        )
