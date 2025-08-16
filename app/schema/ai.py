from datetime import date
from typing import List, Literal, Optional

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


class WritingFeedbackRequest(BaseModel):
    prompt: str
    answer: str
    taskType: Literal["essay", "letter", "report"]


class WritingFeedbackResponse(BaseModel):
    band: float
    comment: str
    task_achievement: str
    coherence_cohesion: str
    lexical_resource: str
    grammatical_range: str
    suggestions: List[str]
    improved_version: str
