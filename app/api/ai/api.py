from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.llm import get_llm_provider
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
    provider = get_llm_provider()
    try:
        text = await provider.generate_text(payload.prompt)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM provider error: {exc}",
        ) from exc

    return {"success": True, "data": {"text": text}}
