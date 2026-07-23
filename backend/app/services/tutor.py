from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

import requests
from sqlalchemy.orm import Session

from backend.app.config import get_settings


conversation_store: dict[str, dict[str, Any]] = {}


class TutorService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()

    def ask_question(self, user_id: str, question: str) -> dict:
        """Process a student question with a Socratic response."""
        conversation_id = str(uuid4())
        response = self._generate_response(question)

        conversation_store[conversation_id] = {
            "user_id": user_id,
            "question": question,
            "response": response,
            "hint_level": 0,
            "created_at": datetime.utcnow(),
        }

        return {
            "conversation_id": conversation_id,
            "response": response,
            "hint_level": 0,
            "can_request_hint": True,
        }

    def get_hint(self, user_id: str, conversation_id: str, hint_level: int = 0) -> dict:
        """Generate a hint for the saved conversation."""
        conversation = conversation_store.get(conversation_id)
        if not conversation or conversation["user_id"] != user_id:
            return {
                "hint": "I couldn't find that conversation. Please ask a new question first.",
                "hint_level": 1,
                "can_request_more_hints": False,
            }

        current_level = conversation.get("hint_level", hint_level)
        next_level = current_level + 1
        question = conversation["question"]

        hint = self._generate_hint(question, next_level)
        conversation["hint_level"] = next_level

        return {
            "hint": hint,
            "hint_level": next_level,
            "can_request_more_hints": next_level < 6,
        }

    def reveal_answer(self, user_id: str, conversation_id: str) -> dict:
        """Reveal a fuller answer for the saved conversation."""
        conversation = conversation_store.get(conversation_id)
        if not conversation or conversation["user_id"] != user_id:
            return {
                "answer": "I couldn't find that conversation.",
                "explanation": "Please ask a new question first.",
            }

        question = conversation["question"]
        answer = self._generate_answer(question)

        return {
            "answer": answer,
            "explanation": "We can build toward the answer by unpacking the question step by step.",
        }

    def _generate_response(self, question: str) -> str:
        """Generate the main tutor response using Gemini or a safe fallback."""
        prompt = (
            "You are a Socratic tutor. Respond with 2-4 short sentences. "
            "Do not give the full answer immediately. Ask guiding questions, "
            "point at useful concepts, and keep the tone encouraging.\n\n"
            f"Student question: {question}"
        )
        gemini_text = self._call_gemini(prompt)
        if gemini_text:
            return gemini_text

        topic = self._extract_topic(question)
        lowered = question.lower()

        if any(keyword in lowered for keyword in ["explain", "teach me", "help me learn", "what is"]):
            return (
                f"Sure — let’s unpack {topic} from the basics. "
                f"I’ll keep it simple first, then we can go deeper. "
                f"What part of {topic} feels most confusing right now?"
            )

        if "how" in lowered:
            return (
                f"Let’s break {topic} into smaller steps. "
                "What outcome are you trying to reach, and what do you already know about the parts involved?"
            )

        if "why" in lowered:
            return (
                f"Good question about {topic}. "
                "What underlying rule or principle do you think might be causing that result?"
            )

        return (
            f"I’m here with you on {topic}. "
            "Can you share a little more context so I can guide you step by step?"
        )

    def _generate_hint(self, question: str, hint_level: int) -> str:
        """Generate a progressively stronger hint."""
        prompt = (
            "You are a tutoring assistant. Give one concise hint only. "
            "Do not reveal the full solution. Make the hint more specific based on the level.\n\n"
            f"Hint level: {hint_level}\n"
            f"Student question: {question}"
        )
        gemini_text = self._call_gemini(prompt)
        if gemini_text:
            return gemini_text

        fallback_hints = {
            1: "Start by identifying the core concept or definition involved.",
            2: "Break the problem into smaller parts and ask what each part needs.",
            3: "Look for a pattern, constraint, or example that matches the idea.",
            4: "Try working through one simple case first.",
            5: "Compare this with a similar problem you already know how to solve.",
            6: "You are very close; focus on the key step that connects the facts.",
        }
        return fallback_hints.get(hint_level, fallback_hints[6])

    def _generate_answer(self, question: str) -> str:
        """Generate a fuller answer for reveal mode."""
        prompt = (
            "You are a helpful tutor. Give the answer in a clear, concise way, "
            "followed by a short explanation.\n\n"
            f"Student question: {question}"
        )
        gemini_text = self._call_gemini(prompt)
        if gemini_text:
            return gemini_text

        return "Here is the direct answer in plain language, followed by a short explanation of the steps."

    def _call_gemini(self, prompt: str) -> str | None:
        """Call the Gemini REST API if a key is available."""
        if not self.settings.gemini_api_key:
            return None

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.settings.gemini_model}:generateContent?key={self.settings.gemini_api_key}"
        )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.settings.gemini_temperature,
                "maxOutputTokens": 512,
            },
        }

        try:
            response = requests.post(url, json=payload, timeout=self.settings.gemini_timeout)
            response.raise_for_status()
            data = response.json()
            candidates = data.get("candidates") or []
            if not candidates:
                return None

            parts = candidates[0].get("content", {}).get("parts", [])
            texts = [part.get("text", "") for part in parts if part.get("text")]
            text = "\n".join(texts).strip()
            return text or None
        except Exception:
            return None

    def _extract_topic(self, question: str) -> str:
        """Best-effort topic extraction for local fallback responses."""
        lowered = question.lower().strip().rstrip("?")
        prefixes = [
            "explain ",
            "teach me ",
            "help me learn ",
            "what is ",
            "what are ",
            "how do i ",
            "how do you ",
            "how to ",
        ]

        for prefix in prefixes:
            if lowered.startswith(prefix):
                return question[len(prefix):].strip(" .!?") or "this topic"

        return question.strip(" .!?") or "this topic"
