import uuid
from typing import List, Optional

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: uuid.UUID
    question: str
    options: Optional[List[str]] = None  # For multiple choice questions
    correct: Optional[int] = None  # Index for multiple choice
    answer: Optional[str] = None  # For completion/short answer
    type: str


class PassageResponse(BaseModel):
    id: uuid.UUID
    title: str
    text: str  # This maps to the 'content' field in the database
    questions: List[QuestionResponse]


class ReadingPassageResponse(BaseModel):
    id: uuid.UUID
    title: str
    passage: str  # This maps to the 'content' field in the database
    questions: List[QuestionResponse]


class ListeningPracticeResponse(BaseModel):
    passages: List[PassageResponse]


class ReadingPracticeResponse(BaseModel):
    passages: List[ReadingPassageResponse]


class SpeakingQuestionResponse(BaseModel):
    id: uuid.UUID
    question: str
    title: str
    part: str
    type: str = "speaking"
    preparationTime: int  # seconds


class SpeakingPracticeResponse(BaseModel):
    questions: List[SpeakingQuestionResponse]


class WritingPromptResponse(BaseModel):
    id: uuid.UUID
    question: str
    title: str
    type: str
    timeLimit: int  # seconds
    wordLimit: str


class WritingPracticeResponse(BaseModel):
    prompts: List[WritingPromptResponse]
