from uuid import uuid4
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.config import get_settings


class TutorService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
    
    def ask_question(self, user_id: str, question: str) -> dict:
        """Process student question with Socratic method."""
        conversation_id = str(uuid4())
        
        # Generate Socratic response
        response = self._generate_response(question)
        
        return {
            "conversation_id": conversation_id,
            "response": response,
            "hint_level": 0,
            "can_request_hint": True
        }
    
    def get_hint(self, user_id: str, conversation_id: str, hint_level: int = 0) -> dict:
        """Generate hint for student."""
        hint_text = f"Here's a hint (level {hint_level + 1}): Think about the fundamentals..."
        
        return {
            "hint": hint_text,
            "hint_level": hint_level + 1,
            "can_request_more_hints": hint_level < 3
        }
    
    def reveal_answer(self, user_id: str, conversation_id: str) -> dict:
        """Reveal full answer."""
        return {
            "answer": "This is the complete answer...",
            "explanation": "Here's how to approach this problem..."
        }
    
    def _generate_response(self, question: str) -> str:
        """Generate Socratic response (using simple logic for now)."""
        if not question or len(question) < 3:
            return "Could you please provide a more detailed question?"
        
        keywords = question.lower().split()
        
        if "what" in keywords:
            return "Great question! Let me ask you: What do you already know about this topic?"
        elif "how" in keywords:
            return "Interesting! Before I explain, can you think of any similar problems you've solved?"
        elif "why" in keywords:
            return "That's a thoughtful question! Have you considered the underlying principles?"
        else:
            return "Tell me more about what you're trying to understand."
