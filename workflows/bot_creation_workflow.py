# botsmith/workflows/bot_creation_workflow.py

from typing import Dict, Any
from botsmith.workflows.base_workflow import BaseWorkflow
from botsmith.core.interfaces.agent_interface import IAgent


class BotCreationWorkflow(BaseWorkflow):
    """
    Workflow for creating a bot using multiple agents.
    """

    def __init__(
        self,
        analyzer: IAgent,
        coder: IAgent,
        validator: IAgent,
    ):
        super().__init__("bot_creation")

        self.analyzer = analyzer
        self.coder = coder
        self.validator = validator

        self.add_step("analyze", self._analyze)
        self.add_step("code", self._code)
        self.add_step("validate", self._validate)

    def _analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = self.analyzer.execute(
            context["prompt"], context
        )
        return {"analysis": result}

    def _code(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = self.coder.execute(
            str(context["analysis"]), context
        )
        return {"code": result}

    def _validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = self.validator.execute(
            str(context["code"]), context
        )
        return {"validation": result}
