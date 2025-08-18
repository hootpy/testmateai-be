import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel


class MockTestSectionResponse(BaseModel):
    id: str
    name: str
    time: str
    questions: int


class MockTestResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    duration: int  # minutes
    sections: List[MockTestSectionResponse]
    createdAt: datetime


class MockTestsListResponse(BaseModel):
    success: bool
    data: List[MockTestResponse]
