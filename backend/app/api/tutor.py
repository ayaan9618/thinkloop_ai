from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.dependencies import get_current_user
from backend.app.services.tutor import TutorService

router = APIRouter(prefix="/tutor", tags=["tutor"])


class AskQuestionRequest(BaseModel):
    question: str


class HintResponse(BaseModel):
    hint: str
    hint_level: int
    can_request_more_hints: bool


class AskResponse(BaseModel):
    conversation_id: str
    response: str
    hint_level: int
    can_request_hint: bool


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ask a question to the tutor."""
    service = TutorService(db)
    result = service.ask_question(current_user.user_id, request.question)
    return AskResponse(**result)


@router.post("/hint/{conversation_id}", response_model=HintResponse)
async def request_hint(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Request a hint for a question."""
    service = TutorService(db)
    result = service.get_hint(current_user.user_id, conversation_id)
    return HintResponse(**result)


@router.post("/reveal/{conversation_id}")
async def reveal_answer(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reveal the answer (only after trying)."""
    service = TutorService(db)
    return service.reveal_answer(current_user.user_id, conversation_id)
