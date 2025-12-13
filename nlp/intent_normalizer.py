from botsmith.nlp.schemas import CommandIntent


class IntentNormalizer:
    """
    Validates, normalizes, and scores parsed intents.
    """

    ALLOWED_INTENTS = {
        "build_bot",
        "deploy",
        "analyze",
        "unknown",
    }

    def normalize(self, raw: dict, text: str) -> CommandIntent:
        intent = raw.get("intent", "unknown")

        if intent not in self.ALLOWED_INTENTS:
            intent = "unknown"

        confidence = float(raw.get("confidence", 0.0))
        entities = raw.get("entities", {})

        ambiguity = None
        if confidence < 0.6:
            ambiguity = "Low confidence intent"

        return CommandIntent(
            intent=intent,
            entities=entities,
            confidence=confidence,
            raw_text=text,
            ambiguity=ambiguity,
        )
