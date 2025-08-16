from typing import List, Literal, Optional

from pydantic import BaseModel


class TestQuestion(BaseModel):
    id: int
    text: str
    topic: str
    difficulty: str
    category: str  # For speaking questions


class SpeakingQuestionsResponse(BaseModel):
    questions: List[TestQuestion]


class TestOption(BaseModel):
    id: str
    text: str


class Question(BaseModel):
    id: int
    text: str
    type: str
    options: Optional[List[TestOption]] = None
    correct: Optional[dict] = None


class ListeningPassage(BaseModel):
    id: int
    title: str
    text: str
    audioUrl: str
    duration: int  # in seconds
    questions: List[Question]


class ListeningPassagesResponse(BaseModel):
    passages: List[ListeningPassage]


class ReadingPassage(BaseModel):
    id: int
    title: str
    text: str
    questions: List[Question]


class ReadingPassagesResponse(BaseModel):
    passages: List[ReadingPassage]


class WritingPrompt(BaseModel):
    id: int
    text: str
    taskType: Literal["essay", "letter", "report"]
    wordLimit: int
    timeLimit: int  # in minutes


class WritingPromptsResponse(BaseModel):
    prompts: List[WritingPrompt]
