from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class CreateBotRequest(BaseModel):
    prompt: str
    project_name: Optional[str] = None

class GenericResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class BotResponse(GenericResponse):
    workflow_name: str
    steps_executed: int
    generated_files: List[Any]
