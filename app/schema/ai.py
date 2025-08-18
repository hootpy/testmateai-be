from pydantic import BaseModel, Field


class GenerateTextRequest(BaseModel):
    prompt: str = Field(min_length=1)
