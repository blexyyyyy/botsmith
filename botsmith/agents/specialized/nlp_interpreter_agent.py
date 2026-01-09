from botsmith.agents.base_agent import BaseAgent
from botsmith.nlp.semantic_parser import SemanticParser
from botsmith.nlp.intent_normalizer import IntentNormalizer


class NLPInterpreterAgent(BaseAgent):
    """
    High-quality NLP interpreter using LLM + validation.
    """

    def __init__(self, llm, memory_manager, **kwargs):
        super().__init__(
            llm=llm,
            memory_manager=memory_manager,
            **kwargs,
        )
        self._parser = SemanticParser(llm)
        self._normalizer = IntentNormalizer()

    def _execute(self, task: str, context):
        parsed = self._parser.parse(task)
        intent = self._normalizer.normalize(parsed, task)

        return {
            "intent": intent.intent,
            "entities": intent.entities,
            "confidence": intent.confidence,
            "ambiguity": intent.ambiguity,
            "raw": intent.raw_text,
        }
