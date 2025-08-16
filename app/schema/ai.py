from typing import List, Optional

from pydantic import BaseModel


class WordFeedback(BaseModel):
    word: str
    native_like: bool
    score: float
    tip: Optional[str] = None


class SpeakingFeedbackRequest(BaseModel):
    question: str
    transcript: str
    audioUrl: Optional[str] = None


class SpeakingFeedbackResponse(BaseModel):
    band: float
    comment: str
    words: List[WordFeedback]
    length_feedback: str
    suggestions: List[str]
    pronunciation_tips: List[str]
    grammar_feedback: str
    vocabulary_feedback: str
    coherence_feedback: str
