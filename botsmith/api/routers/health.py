from fastapi import APIRouter
from botsmith.api.schemas import GenericResponse

router = APIRouter()

@router.get("/health", response_model=GenericResponse)
def health_check():
    return GenericResponse(status="ok", message="BotSmith API is running")
