import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class VocabularyResponse(BaseModel):
    id: uuid.UUID
    word: str
    definition: Optional[str]
    source: str
    reviewed: bool
    mastered: bool
    notes: Optional[str]
    createdAt: datetime


class VocabularyListResponse(BaseModel):
    success: bool
    data: List[VocabularyResponse]


class AddVocabularyRequest(BaseModel):
    words: List[str]
    source: str  # practice|mock_test|manual
    context: Optional[str] = None


class AddedVocabularyResponse(BaseModel):
    id: uuid.UUID
    word: str
    source: str
    createdAt: datetime


class AddVocabularyResponse(BaseModel):
    addedWords: int
    duplicateWords: int
    words: List[AddedVocabularyResponse]


class UpdateVocabularyRequest(BaseModel):
    reviewed: Optional[bool] = None
    mastered: Optional[bool] = None
    notes: Optional[str] = None


class UpdateVocabularyResponse(BaseModel):
    id: uuid.UUID
    word: str
    reviewed: bool
    mastered: bool
    notes: Optional[str]
    updatedAt: datetime
