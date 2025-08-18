from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.llm import generate_text_response
from app.core.config import SETTINGS
from app.core.depends.get_session import get_session
from app.schema.ai import GenerateTextRequest

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
)


@router.post("/generate_text")
async def generate_text(
    payload: GenerateTextRequest,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    # db is injected to keep the signature consistent with other endpoints; not used currently
    try:
        result = await generate_text_response(SETTINGS, user_prompt=payload.prompt)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM provider error: {exc}",
        ) from exc

    return {"success": True, "data": result}
